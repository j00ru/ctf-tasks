# Pipeline

| Task             | Pipeline                   |
|------------------|----------------------------|
| Competition      | [Dragon CTF 2018](https://ctftime.org/event/649)            |
| Location				 | Warsaw, Poland				 		  |
| Category         | Exploitation / Programming |
| Platform         | Linux x64                  |
| Scoring          | 340 pts (easy/medium)      |
| Number of solves | 5 out of 13 teams          |

## Description

So you think you're good at programming? Try this!

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

The task is a x64 ELF file with all mitigations enabled (NX, PIE, RELRO etc.), and the teams are provided the executable, which they have to reverse engineer. There, they can find that:

1. The server accepts programs written in the esoteric [Befunge](https://en.wikipedia.org/wiki/Befunge) language, which executes on a 2D matrix. The maximum size of the program is 80x25. The `'.'` and `'&'` instructions for loading/printing integers are not supported.
2. The server runs 20 tests against the user-supplied program. In each test, the input is a randomly generated expression using arithmetic and binary operators, such as addition, multiplication, exponentation, or, xor and left/right rotate. An example expression could be `1+2^3|4x5<6>7`. Each expression is maximum 16 bytes in length.
3. The server expects the Befunge program to calculate the value of the expression and output it in ASCII form.
4. If all 20 tests pass, the user receives the flag.

Writing such a calculator in Befunge seems to be a very difficult task, especially considering that it doesn't natively support bit operations such as or, xor or rot. The players might be tempted to try to do it, and who knows, maybe some of them will succeed. :) (I hope not as it should be nearly impossible given the constraints).

The trick is that there is an out-of-bounds read in the "read input" instruction, and the program can read beyond just the input expression. The expressions are stored in `std::string` objects, but because they are always <= 16 bytes in length, the data is always stored within the object itself and not in a separate heap allocation. In this case, it's on the stack.

Coincidentally, the expected value of the expression is also stored on the stack as an integer. The user's program can access it with enough invocations of the `~` instruction. Once this is done, it is necessary to convert it to a string (i.e. implement an `itoa()` functionality), skip the leading zeros, and output the meaningful digits back to the server. An example program which achieves this can be found in [exploit.txt](solution/exploit.txt).

</p>
</details>
