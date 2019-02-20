# Production

| Task             | Production                |
|------------------|---------------------------|
| Competition      | [Teaser Dragon CTF 2018](https://ctftime.org/event/648)    |
| Location				 | Online 									 |
| Category         | Software exploitation     |
| Platform         | Linux x64                 |
| Scoring          | 343 pts (easy/medium)     |
| Number of solves | 16 out of 233 teams       |

## Description

Can you spot any problems with the production-level quality of our lyrics explorer code?

## Solution summary

<details><summary>Click to expand</summary>
<p>

The task is a x64 ELF file with all mitigations enabled (NX, PIE, RELRO etc.), and the teams are provided the original source code of the program. It allows the user to browse the lyrics of some rock bands' songs. The exploitation process is as follows:

1. List the contents of the task's cwd through a one-level path traversal, thanks to a bug in the "songs" operation ("songs .."). This lets you see that the flag can be found in the "flag" file.
2. The intended bug is that when you try to read a file which contains the string "DrgnS", the `assert(close(globals::records[idx]) == 0);` code is executed, which looks like it closes the file descriptor, but because it is compiled in release mode (see the `-DNDEBUG` flag), the whole expression inside of `assert()` is not included in the executable, resulting in a concealed fd leak.
3. In `set_limits()`, we set the maximum number of open fds in the process to 32. This means that any potential fd leak can quickly exhaust the fd quota for the process.
4. The "flag" file cannot be used for the fd leak, because the "flag" word is filtered in the paths of opened lyrics files. However, the "lyrics" task executable also contains the "DrgnS" string, which makes it feasible to use through a "open .. lyrics" command followed by a few reads from the file.
5. Thanks to the leak, we can cause the first `open()` in `open_lyrics()` to succeed, but the second one to fail. This enables us to skip the check for the "flag" word in the file path, making it possible to plant an fd to the flag file in the records list.
6. We still cannot read the flag directly from the file because of the logic in `read_lyrics()`, but we can load the flag into the static buffer.
7. At the end, we try to read the contents of a lyrics file which was already fully read before (i.e. is currently at EOF), which results in `read_lyrics()` printing out the leftover string in the static buffer, which happens to be the flag.

</p>
</details>

## External write-ups

1. https://ctftime.org/writeup/11454
2. https://changochen.github.io/2018-09-29-Teaser-Dragon-CTF-2018.html
