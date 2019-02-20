# Basic information

| Task             | Memory                   |
|------------------|--------------------------|
| Competition      | CONFidence CTF 2014      |
| Location				 | Krakow, Poland						|
| Category         | Reverse engineering      |
| Platform         | Windows x86              |
| Scoring          | 50 pts (easy)				    |
| Number of solves | 2 out of 11 participants |

## Description

Destruction is key.

## Solution summary

<details><summary>Click to expand</summary>
<p>

1. Unpack a slightly corrupted UPX-packed executable.
2. Reverse engineer a very simple virtual machine implemented in the challenge, consisting mostly of arithmetic and binary operators.
3. Calculate the textual string expected by the VM program, either by reversing all operations or brute-forcing the value of each byte.
4. Notice that with the correct input, the real flag is constructed in memory in a destructor routine.

</p>
</details>
