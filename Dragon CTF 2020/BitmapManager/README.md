# BitmapManager

| Task             | BitmapManager              |
|------------------|----------------------------|
| Competition      | [Dragon CTF 2020](https://ctftime.org/event/1082)            |
| Location         | Online                     |
| Category         | Exploitation               |
| Platform         | Windows x64                |
| Scoring          | 485 pts (hard)             |
| Number of solves | 2 out of 539 teams         |

## Description

Here's a software solution that meets all of your image management needs! It was written in C++ to achieve the highest levels of performance, but worry not, we have enabled some of the latest and greatest compiler options to ensure that memory corruption is not a concern.

## Hint

<details><summary>Click to expand</summary>
<p>

Loading the flag in memory is half the battle. Now how can you get it out of there?

</p>
</details>

## Solution

<details><summary>Click to expand</summary>
<p>

The task is a x64 Windows executable exposed over the network. It is an "image management" program allowing the user to load bitmaps from disk and from standard input, merge them together, and print them out. It is compiled with AddressSanitizer, which was [recently added](https://devblogs.microsoft.com/cppblog/addresssanitizer-asan-for-windows-with-msvc/) to Visual Studio.

```
C:\> BitmapManager.exe
[ASAN protection:    ON ]
[ASAN crash reports: OFF]
Supported options:
  list_builtins : List builtin bitmaps
  list          : List currently loaded bitmaps
  load_builtin  : Load a builtin bitmap
  load          : Load a bitmap from memory
  merge         : Merge two bitmaps into one
  dump          : Print out a bitmap
  unload        : Unload a bitmap
  help          : Print this message
  exit          : Exit program
Option:
```

Due to the fact that there aren't many serious memory corruption vulnerabilities in the code (that I know of) and ASAN is enabled, getting remote code execution shouldn't be possible. However, ASAN doesn't protect very well against the use of uninitialized memory from the stack, and this is what has to be exploited here. The contents of the flag can be easily read into the stack by abusing a path traversal bug and attempting to load `../flag.txt` with the `load_builtin` command. We can then proceed to leak it from there.

There are two bugs planted in the decompression of 8-bit RLE streams. The first one is an off-by-one overread of the argument of the absolute mode marker (byte 0x00), and the second one is a late bounds check after already having performed a potentially memory-corrupting `memcpy()` in the absolute mode. By combining the two issues, it is possible to overlap a byte of the flag with the out-of-bounds size of the absolute mode chunk, and have it used as a `memcpy()` length to an arbitrarily sized destination buffer. In such case, the stack layout of the `load` option handler looks roughly as follows:

```
[            Input bitmap (8-bit RLE compressed)            ][  Leftover flag contents   ]
+------------------+------------------+---------------+------+---+---+---+---+---+---+----
| BITMAPFILEHEADER | BITMAPINFOHEADER | Color palette | 0x00 | D | r | g | n | S | { | ...
+------------------+------------------+---------------+------+---+---+---+---+---+---+----
```

Depending on whether the `memcpy()` exceeds the bounds of the buffer or not, the process will be terminated by ASAN or continue running. Normally, when an invalid memory access is detected, the remote client would receive the full ASAN report including the size of the faulty `memcpy()`, which is the same as one character of the flag. In order to prevent this simple information disclosure, the application closes the `stderr` stream at the beginning of `main()`, so all the user sees is the connection either terminating or staying alive with an error message sent by the program. Nevertheless, this observable behavior can still be used to construct an oracle that evaluates the expression `flag[x] >= y`. 

With the help of the oracle, one can determine the value of each byte of the flag in 7 iterations with binary search. In my experiments, the exploit takes around 15 seconds to leak out the complete flag on localhost.

</p>
</details>

## External write-ups

1. https://faraz.faith/2020-11-23-dragonctf-bitmapmanager/
