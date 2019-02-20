# Basic information

| Task             | Bubblegum                                      |
|------------------|------------------------------------------------|
| Competition      | [Teaser CONFidence CTF 2016](https://ctftime.org/event/307)                     |
| Location				 | Online															 	          |
| Category         | Software exploitation                          |
| Platform         | Windows x86                                    |
| Scoring          | 500 pts (hard)					                        |
| Number of solves | 0 out of 44 teams (1 after the end of the CTF) |

## Description

Here's something new, a Windows challenge for your amusement! :-)

## Solution summary

<details><summary>Click to expand</summary>
<p>

The challenge is a 32-bit Windows task with all security options enabled, no symbols and no helper messages. It uses a custom heap and a custom implementation of buffers with builtin bounds checking using the x86 `BOUND` instruction. The custom allocator operates on an RWX memory mapping which facilitates exploitation.

Exploitation:
1. Use of uninitialized memory (using the custom allocator) in the implementation of so-called `CompactArrays` makes it possible to set element width to 3 (normally only 1, 2 and 4 are allowed).
2. In the `memset()`-like operator there is a bug in calculating the distance between two pointers to triplets (24-bit values achieved thanks to point (1)), which may result in a small buffer overflow on the custom heap.
3. The buffer overflow can be used to overwrite the bounds of `SafeBuffer`, allowing for an arbitrary, relative write primitive.
4. The image base of the task program is saved in the first 4 bytes of the allocator mapping. They have to be leaked, which is achieved byte by byte (two bytes in total, because the least significant 16 bits on Windows are always 0), by redirecting a `SafeBuffer*` to overlap with the disclosed byte, and attempt to write to such SafeBuffer with descending 0xff => 0x00 indexes. Once the connection is dropped, we know we have found the correct byte. Since the base address of the executable doesn't change between connections, we can reliably leak it in several connections.
5. The address of the custom allocator's memory region must also be leaked, which is easily achieved by shifting the pointer of a `SafeBuffer` to overlap with a `CompactArray` structure.
6. With both addresses known, the relative write can now be used to overwrite a top level exception handler saved in static memory. It is overwritten to point at shellcode set up in the custom allocator area.
7. Lastly, an exception is triggered, which redirects execution to our shellcode, which opens `flag.txt`, reads the flag to memory and prints it out.

</p>
</details>
