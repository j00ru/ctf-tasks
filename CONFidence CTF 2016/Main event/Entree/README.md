# Basic information

| Task             | Entree                      |
|------------------|-----------------------------|
| Competition      | [CONFidence CTF 2016](https://ctftime.org/event/308)         |
| Location				 | Krakow, Poland					 		 |
| Category         | Software exploitation       |
| Platform         | Windows x86                 |
| Scoring          | 250 pts (medium difficulty) |
| Number of solves | 1 out of 22 teams           |

## Description

If you've had your starter, it's time for an entree! I'm sure you've come prepared for some Windows pwning. :)

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

There are two bugs designed to solve this challenge (there may be some other ones which should not make it possible to solve the task):

  1. A format string bug which can be used to leak data from the stack (%n is disabled on Windows, so writing is not possible).
  2. A NULL pointer dereference with a controlled index, which can be used for an arbitrary write.

There is also an unhandled exception handler which allows for one exception to occur before terminating the application.

An example way to solve the challenge:

  1. Leak the base address of the image and the stack address using the format string bug.
  2. Write ROP on the stack at the address of the restarted main() stack frame, such that when it returns, it starts to execute the ROP.

In my opinion, the ROP itself is not trivial (`LoadLibrary` is disabled by AppJailLauncher, `VirtualAlloc`/`VirtualProtect` are not available, the return value of `CreateFile` must be passed as argument to `ReadFile` etc.), but it essentially boils down to `CreateFile`, `ReadFile`, `GetStdHandle`, `WriteFile`, `Sleep` and `ExitProcess`. Please refer to the exploit for details.

</p>
</details>
