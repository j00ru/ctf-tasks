# Basic information

| Task             | Quarantine                 |
|------------------|----------------------------|
| Competition      | [Teaser CONFidence CTF 2015](https://ctftime.org/event/205) |
| Location				 | Online											|
| Category         | Software exploitation      |
| Platform         | Linux x64                  |
| Scoring          | 500 pts (hard)						  |
| Number of solves | 5 out of 160 teams         |

## Description

The developers of this service think they have found a way to automatically thwart all memory corruption attacks. Can you prove them wrong?

## Solution summary

<details><summary>Click to expand</summary>
<p>

1. Leak the address of the stack shadow memory by invoking the `give_me_the_flag` command.
2. Exploit a use-after-free vulnerability of the `vm::VMState` object through a dangling pointer in the `globals::current_vm` pointer, when all virtual machines are removed. By filling up the ASAN quarantine (adjusted to 1 MB during the CTF instead of the default 256 MB settings), we can replace the freed `vm::VMSTate` object, and use it to zero-out arbitrary memory regions.
3. Zero out the shadow memory of the operation string buffer, and leak the shadow memory address of the buffer where the flag is loaded by `give_me_the_flag`.
4. Zero out the second shadow memory using the same UAF bug, and successfully retrieve the flag.

</p>
</details>

## External write-ups

1. http://int3pids.blogspot.com/2015/04/confidence-2015-teaser-quarantine-write.html
