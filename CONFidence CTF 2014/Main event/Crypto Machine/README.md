# Crypto Machine

| Task             | Crypto Machine              |
|------------------|-----------------------------|
| Competition      | CONFidence CTF 2014         |
| Location				 | Krakow, Poland							 |
| Category         | Software exploitation       |
| Platform         | Linux x64                   |
| Scoring          | 200 pts (medium difficulty) |
| Number of solves | 0 out of 11 participants    |

## Description

The crypto machine will hash for you, but will it drop the flag?

## Solution summary

<details><summary>Click to expand</summary>
<p>

1. Exploit the `abs()` related logic by specifying operation index `0x8000000000000000` to get access to the special HMAC functionality (operation #0).
2. Send only 2 bytes of the input key length (instead of the full 4), which results in bypassing the sanity check of the variable.
3. Perform a partial, 2-byte overwrite of the `EVP_md5` function pointer on the stack, to redirect it to a `system("/bin/sh")` call. Because we haven't defeated ASLR and the most significant nibble (4 bits) of the overwritten memory is randomized, it is necessary to run the exploit in a loop, hoping for it to succeed after a few (or a few dozen) attempts at most.

</p>
</details>
