# Basic information

| Task             | Multipurpose Calculation Machine |
|------------------|----------------------------------|
| Competition      | Teaser CONFidence CTF 2014       |
| Location				 | Online							  						|
| Category         | Software exploitation            |
| Platform         | Linux x86                        |
| Scoring          | 200 pts (medium difficulty)      |
| Number of solves | 14 out of 99 participants        |

## Solution summary

<details><summary>Click to expand</summary>
<p>

Under specific conditions, `strncpy` doesn't nul-terminate the output buffer, leading to a format string vulnerability. [Our exploit](solution/exploit.py) uses it to leak the program base address, and overwrite the `exit` function pointer in `.got.plt` with the address of a `system("/bin/sh")` call found in the challenge, to get access to the shell.

</p>
</details>

## External write-ups 

1. https://github.com/0xddaa/blog/blob/master/content/2014/dsctf-pwn-200-calc-machine.md
2. http://balidani.blogspot.com/2014/04/confidence-ds-ctf-pwn200-writeup.html
3. https://github.com/gynvael/stream/tree/master/000-pwn200-format-bug and https://www.youtube.com/watch?v=hQnPlC1eTuc (PL)
