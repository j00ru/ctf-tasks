# Basic information

| Task             | Fastcalc                   |
|------------------|----------------------------|
| Competition      | [Teaser CONFidence CTF 2017](https://ctftime.org/event/433) |
| Location				 | Online 										|
| Category         | Software exploitation      |
| Platform         | Windows x86                |
| Scoring          | 500 pts (hard) 					  |
| Number of solves | 11 out of 258 teams        |

## Description

What would a CONFidence CTF be without a Windows-hosted exploitation challenge? :) This time you're facing a fast, greatly optimized calculator capable of concurrently evaluating multiple expressions. In fact it is so technically advanced that it will only run on CPUs supporting the cutting-edge SSE2 extension. Do you think you can hack it?

## Solution summary

<details><summary>Click to expand</summary>
<p>

A regular 32-bit Windows binary with a typical set of mitigations (ASLR, DEP, /GS), but nothing out of the ordinary (no CFG, RFG etc.). It is a "multithreaded" evaluator of arithmetic expressions (e.g. (1+2\*3)/4), which uses the Fibers Windows-specific mechanism to switch between calculations. It uses the XMM0-7 (SSE2) registers to perform the computation. It is statically linked and has a `system` call to make exploitation easier.

There are two bugs:
1. Semi-continuous stack buffer overflow in converting the infix representation of the expression to the Reverse Polish Notation one. It's in the stack frame of the `main` function. However, since the overflowing structures have large alignment holes, it is possible to leave the stack cookie intact, but overwrite the return address of the function.
2. The XMM context is not switched between executions of fibers. When the src and dst addresses of `memcpy` have the same 16-byte alignment, the function uses the XMM registers to transfer data in memory, and then doesn't clean them up. While `std::cout` zeros XMM0-XMM5, XMM6-7 keep the left-over values used by `memcpy`. These values can then be leaked through the calculation results of worker fibers, and may disclose information such as the image base address or stack address.

The exploitation process is as follows (see [exploit.py](solution/exploit.py) for more details).
1. Create a "++++++" expression, which will be later used to read the value of the XMM6 register and return it as the output (through XMM0).
2. Create a "+"x256 expression. When its RPN representation is copied from stack to heap, and if the addresses align correctly, `memcpy` leaks a valid code pointer through XMM6.
3. Run the evaluation of both expressions, which will yield the leaked pointer as the output of the 1st one (or junk bytes, in which case we have to reconnect and try again).
4. Create an expression of "0+"x131 followed by a 64-bit double-encoded ROP chain making up `system("cmd.exe")`. This will keep the original value of the stack cookie, but overwrite the return-address and one dword after it.
5. Call "quit", which will trigger the mini-ROP and invoke a shell.

Now we can type in `type flag.txt` and the flag is ours. :)

</p>
</details>

## External write-ups

1. https://github.com/chksum0/writeups/tree/master/confidence_teaser_2017/fastcalc
2. https://dougallj.wordpress.com/2017/04/03/quick-writeups-from-teaser-confidence-ctf-2017/
