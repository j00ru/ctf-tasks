# Basic information

| Task             | Night Sky                 |
|------------------|---------------------------|
| Competition      | [CONFidence CTF 2015](https://ctftime.org/event/206)       |
| Location				 | Krakow, Poland						 |
| Category         | Software exploitation     |
| Platform         | Linux x64                 |
| Scoring          | 500 pts (hard) 					 |
| Number of solves | 2 out of 11 teams         |

## Description

The night is dark and full of terrors... or errors? Probably both. Use the force to manage stars and constellations on the sky, Harry, and let the odds be ever in your favor.

## Solution

See the [slides](solution/slides.pdf), or a short summary below.

<details><summary>Click to expand</summary>
<p>

1. Insert a `LIBC_FATAL_STDERR_=1` string into static memory via a new constellation's name.
2. Leak the address of a static buffer with controlled data via the `edit_star` operation, which doesn't properly nul-terminate the name buffer, and then `list_stars` in order to retrieve it back.
3. Trigger a non-exploitable stack-based buffer overflow in the `register_program` function via `n=0`, setting `argv[0]` to the address of a secret (serial number) in static memory, and `envp[]` to `{"LIBC_FATAL_STDERR_=1", NULL}`. This will result in triggering SSP and leaking the secret serial number.
4. Reconnect to the server, and register the program using the leaked secret. This will make it possible to trigger another stack-based buffer overflow in the `save_to_file` operation. Since a structure is overrun, SSP does not protect against overwrites of function pointers residing after the buffer. Now, two paths can be taken: either construct a ROP based on gadgets found in the challenge binary, or simply use a partial overwrite of the `canonicalize_file_name` pointer. As it turns out, the `system()` and `canonicalize_file_name()` functions have the same 2 upper bytes of address (they reside within 64kB of each other).

</p>
</details>
