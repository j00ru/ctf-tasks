# Basic information

| Task             | Antipasto               |
|------------------|-------------------------|
| Competition      | [CONFidence CTF 2016](https://ctftime.org/event/308)     |
| Location				 | Krakow, Poland					 |
| Category         | Software exploitation   |
| Platform         | Linux x86               |
| Scoring          | 50 pts (easy)					 |
| Number of solves | 5 out of 22 teams       |

## Description

A nice and easy exploitation challenge to start off your day in a good mood. Enjoy!

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

The bug is in the `main()` function, which allows an arbitrary size to be passed to `ReadBytes()`, and in `ReadBytes()`, which does not verify the return value of the `read()` function (against -1). With these two things combined, it is possible to cause a static buffer underflow condition, which can be used to overwrite the `.got.plt` `write()` entry
with the address of shellcode, also in static memory (NX and PIE are both
disabled in this challenge).

</p>
</details>
