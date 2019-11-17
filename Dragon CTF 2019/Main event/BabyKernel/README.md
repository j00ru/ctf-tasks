# BabyKernel

| Task             | BabyKernel                 |
|------------------|----------------------------|
| Competition      | [Dragon CTF 2019](https://ctftime.org/event/887)            |
| Location				 | Warsaw, Poland				 		  |
| Category         | Exploitation               |
| Platform         | Windows x64                |
| Scoring          | 460 pts (medium)           |
| Number of solves | 2 out of 14 teams          |

## Description

I think it's nice that Windows exploitation CTF tasks are gaining in popularity. Now it's time to promote Windows ring-0 security too, and what better chance for it than Dragon CTF 2019! Let's get you started with a baby kernel challenge :)

## Setup

During the CTF, the challenge was running on Windows Server 1809 x64. In order to load the `SecureDrv.sys` driver, disable the Driver Signature Enforcement mechanism from an elevated command prompt:

```
>bcdedit /set testsigning on
```

Then reboot the system, and register a service (again from an elevated prompt), e.g.:

```
>sc create SecureDrv binPath=C:\Users\test\Desktop\SecureDrv.sys type=kernel
```

and start it:

```
>sc start SecureDrv
```

Now you should be able to run `SecureClient.exe` and see the following output:

```
>SecureClient.exe
---===[ SecureStorage Client, Dragon CTF 2019 ]===---
[ ] Protect, unprotect?
```

If you wish to accurately model the CTF conditions, you can also configure Windows to automatically reboot on BSoD:

```
>wmic RecoverOS set AutoReboot = True
```

Then create a normal user called "ctf", and create a `C:\flag.txt` file with any access denied for that user. Now you're all set and ready to pwn!

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

The task is a 64-bit Windows kernel driver (`SecureDrv.sys`), loaded in the VM that the player is supposed to exploit. The goal is to elevate one's privileges in the system through a bug in the driver, and read the flag hidden in `C:\flag.txt`, which is normally not accessible. The `SecureDrv.sys` and `SecureClient.exe` (an example client application) files are provided.

A user-mode program communicates with the driver with IOCTLs sent to the `\\.\SecureStorage` interface. There are three operations defined, all of them implemented with `METHOD_NEITHER` (meaning that unsanitized user-mode pointers are passed to the handlers):

 - `MODE_PROTECT`
 - `MODE_UNPROTECT`
 - `PERFORM_OPERATION`

In this case, "protection" means copying a specific user memory region to kernel-mode and erasing the ring-3 area, while unprotecting means copying the previously saved data back to the program's address space. The first two IOCTLs are responsible for switching between operations, while the third one actually triggers their logic. Internally, the mode-switching is achieved by overwriting a static function pointer, which `PERFORM_OPERATION` then calls. This is a pretty useful exploitation primitive in itself.

The actual vulnerability is found in the "unprotect" handler, in the following line:

```C
ProbeForWrite(OutputBuffer, OutputSize + 1, 1);
```

The `OutputSize` is an attacker-controlled `ULONG` variable. When it is set to 0xFFFFFFFF, then the overall `OutputSize + 1` expression overflows and evaluates to 0. When 0 is passed as the `Length` argument to `ProbeForWrite`, the function returns immediately, without performing any sanitization of the `OutputBuffer` pointer at all. In other words, a kernel-mode pointer will pass the validation too.

On the other hand, an `OutputSize` value of 0xFFFFFFFF does not prevent the copying of the output buffer to the specified address; we can still write our previously saved data there. This equips us with a convenient write-what-where primitive, with the "what" being a controlled C-string.

Thanks to the fact that we are logged in as a local user, our processes run with Medium integrity level and therefore have access to the kernel address space information provided by `NtQuerySystemInformation`, such as driver image bases returned by the `SystemModuleInformation` class.

My intended process of exploitation is as follows:

 - Get the base addresses of `ntoskrnl.exe` and `SecureDrv.sys` in the kernel space.
 - Use the write-what-where condition to overwrite the static function pointer in `SecureDrv.sys` with the address of `nt!ExAllocatePoolWithTag`.
 - The function pointer is called with two user-controlled arguments, and its return value is propagated back to ring-3. Thus, we can now allocate a writeable/executable region of kernel memory via `ExAllocatePoolWith(NonPagedPool, 0x1000)` and obtain its address. This enables us to bypass SMEP by not having to execute any kernel code in the user address space.
 - Write shellcode (in this case -- copying the security token from the System process to the exploit process) to the newly allocated R/W kernel memory.
 - Overwrite the operation handler with the address of the payload.
 - Trigger the operation handler, have our shellcode executed, and return with NT AUTHORITY/SYSTEM privileges.
 - Spawn a command prompt and let the user read the flag. :)

I followed a very similar set of steps while working on the "Searchme" challenge during WCTF 2018. You can find a detailed write-up here: https://j00ru.vexillium.org/2018/07/exploiting-a-windows-10-pagedpool-off-by-one/.

Of course a write-what-where condition makes it possible to compromise the kernel in a variety of ways, but the above is probably the simplest one.

Here's an example output of my exploit running:

```
---===[ Baby Kernel Exploit, Dragon CTF 2019 ]===---
[+] ntoskrnl: fffff8062baad000, driver: fffff803926e0000
[+] Operation handler overwritten with nt!ExAllocatePoolWithTag
[+] Allocated shellcode address: ffff9805d64ec001
[+] Wrote shellcode bytes to the allocated address
[+] Operation handler overwritten with shellcode address, invoking the payload...
[+] Done, spawning an elevated command prompt:
Microsoft Windows [Version 10.0.17763.805]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>whoami
nt authority\system

C:\>type C:\flag.txt
DrgnS{Kernel_exploitation_is_twice_the_fun!}
C:\>
```

</p>
</details>
