# Basic information

| Task             | Filesystem                  |
|------------------|-----------------------------|
| Competition      | [CONFidence CTF 2017](https://ctftime.org/event/434)         |
| Location				 | Krakow, Poland					 		 |
| Category         | Software exploitation       |
| Platform         | Linux x64                   |
| Scoring          | 250 pts (medium difficulty) |
| Number of solves | 5 out of 22 teams           |

## Description

We know that securely granting remote access to filesystems is a difficult task, but with our great combination of black- and white-listing solutions, we believe we have all bases covered. To show you how confident we are in our code, we've even put the flag in a local file. It's up for grabs.

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

The task is a x64 ELF file with all mitigations enabled (NX, PIE, RELRO etc.). It makes it possible to perform the following operations against files with arbitrary paths:
  * `read`
  * `write`
  * `lseek`

However, it is only allowed to interact with the `/dev/null` and `/dev/urandom` paths, and when a "flag" substring is detected, the program exits. Internally, the task maintains a cache of 16 file descriptors in the form of a path ---> fd associative array. Arbitrary entries can be inserted into the array as long as the corresponding file can be opened (the whitelist checking is performed after the `open` call).

When the cache becomes larger than 16 items, it is flushed: all file descriptors are closed and all entries removed. THERE IS ONE EXCEPTION: if a specific path was interacted with more times than the rest of the files cumulatively (i.e. it is a "hot path"), it is not removed from the cache, but the fd is still closed. This leads to a situation where the cache entry points into a dangling fd, which can be allocated to another file, causing a "Use-After-Close" condition (basically an UAF on file descriptors).

This can be used to link the `/dev/{null,urandom}` path to a `/proc/self/maps` fd in the cache and subsequently read the process address space layout. We can then create yet another link to `/proc/self/mem`, seek to the right position and directly overwrite the program code with our shellcode. We then get shell, list files in the current directory and read the flag from `find_the_flag_here.txt`.

For specific implementation details, see [exploit.py](solution/exploit.py).

</p>
</details>
