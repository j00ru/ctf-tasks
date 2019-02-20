# Fastcalc-hardened

| Task             | Fastcalc-hardened         |
|------------------|---------------------------|
| Competition      | [CONFidence CTF 2017](https://ctftime.org/event/434)       |
| Location				 | Krakow, Poland					   |
| Category         | Software exploitation     |
| Platform         | Windows x86               |
| Scoring          | 500 pts (hard)						 |
| Number of solves | 3 out of 22 teams         |

## Description

Perhaps you still remember the "Fastcalc" challenge from this year's CONFidence Teaser (see the fastcalc.exe file). Well, we have taken a careful look at the code and your feedback, and think we've fixed the issues that made it so easily exploitable. Most notably, one of the problems was that an innocent input (see [bad_input.txt](task/bad_input.txt)) would sometimes cause the program to return unexpected results. Now that it is resolved, the program surely cannot be pwned anymore? :-)

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

The task is based on the "fastcalc" challenge from CONFidence Teaser 2017. The main changes with relation to the original task are as follows:
* The layout of the stack was rearranged so that:
  * there are no `std::string` objects after the overwritten RPN array, which makes it impossible to disclose stack memory by corrupting the expression string.
  * the controlled 64-bit double value overlaps with EBP+RET instead of RET+ARG, which makes it impossible to just brute-force the binary image base (because it is still necessary to know another address to pivot the stack to).
* The XMM0-XMM7 registers are zeroed out at the beginning of each fiber, disabling simple leaks. HOWEVER, leaks are still possible as the XMM registers are not saved/restored while switching between already running fibers.

The modifications are designed to force the user to use the XMM/memcpy leak to find the base address and stack address, and to create a `system("cmd.exe")` ROP based on that. The existence of the leak is even mentioned in the task description itself.

The exploitation process is as follows (see [exploit.py](solution/exploit.py) for more details).
1. Create a "+"x106 expression, which will be later used to read the value of the XMM6 register and return it as the output (through XMM0).
2. Run the expression, which will execute the first 100 + signs and return to the scheduler fiber.
3. Create a "+"x256 expression. When its RPN representation is copied from stack to heap, and if the addresses align correctly, `memcpy` leaks a valid code pointer through XMM6.
4. Run both expressions again, which should result in expression #1 leaking the value of XMM6 through its output. This gives us the (persistent) image base address. If leaking failed (because of misaligned `memcpy` arguments), reconnect and try again.
5. Repeat the same procedure from steps 1-4 to leak the stack address, but with the #2 expression consisisting of 248 "+" signs instead of 256.
4. Create an expression of a 64-bit double-encoded `system("cmd.exe")` ROP, followed by "+"x258, followed by a 64-bit double-encoded 1-st stage ROP to pivot the stack to the 2-nd stage ROP. This will keep the original value of the stack cookie, but overwrite the EBP pointer and main() return address.
5. Call "quit", which will trigger the 1-st stage ROP, which will transfer execution to the `system("cmd.exe")` ROP and invoke a shell.

Now we can type in `type flag.txt` and the flag is ours. :)

</p>
</details>
