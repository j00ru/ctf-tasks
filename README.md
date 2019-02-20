# CTF Challenges

This repository contains an archive of CTF challenges I developed in the last few years for various CTFs organized by my team – [Dragon Sector](https://dragonsector.pl/). They are mostly software exploitation tasks with varying difficulty levels, for the x86/x64 architectures and Windows/Linux operating systems. Each subdirectory contains basic task information, original description, solution in the form of a short summary or a few slides from the post-CTF presentation, exploit code and optionally links to external solutions.

The challenges are as follows:

| Name                             | Competition                  | Category                   | Platform | Arch. | Difficulty  |
|----------------------------------|------------------------------|----------------------------|----------|-------|-------------|
| [Pipeline](Dragon%20CTF%202018/Main%20event/Pipeline)                         | Dragon CTF 2018              | Exploitation / Programming | Linux    | x64   | Easy/medium |
| [Production](Dragon%20CTF%202018/Teaser/Production)                       | Dragon CTF 2018 (Teaser)     | Exploitation               | Linux    | x64   | Easy/medium |
| [Filesystem](CONFidence%20CTF%202017/Main%20event/Filesystem)                       | CONFidence CTF 2017          | Exploitation               | Linux    | x64   | Medium      |
| [Fastcalc-hardened](CONFidence%20CTF%202017/Main%20event/Fastcalc-hardened)                | CONFidence CTF 2017          | Exploitation               | Windows  | x86   | Hard        |
| [Fastcalc](CONFidence%20CTF%202017/Teaser/Fastcalc)                         | CONFidence CTF 2017 (Teaser) | Exploitation               | Windows  | x86   | Hard        |
| [Entree](CONFidence%20CTF%202016/Main%20event/Entree)                           | CONFidence CTF 2016          | Exploitation               | Windows  | x86   | Medium      |
| [Antipasto](CONFidence%20CTF%202016/Main%20event/Antipasto)                        | CONFidence CTF 2016          | Exploitation               | Linux    | x86   | Easy        |
| [Bubblegum](CONFidence%20CTF%202016/Teaser/Bubblegum)                        | CONFidence CTF 2016 (Teaser) | Exploitation               | Windows  | x86   | Hard        |
| [Night Sky](CONFidence%20CTF%202015/Main%20event/Night%20Sky)                        | CONFidence CTF 2015          | Exploitation               | Linux    | x64   | Hard        |
| [Quarantine](CONFidence%20CTF%202015/Teaser/Quarantine)                       | CONFidence CTF 2015 (Teaser) | Exploitation               | Linux    | x64   | Hard        |
| [Crypto Machine](CONFidence%20CTF%202014/Main%20event/Crypto%20Machine)                   | CONFidence CTF 2014          | Exploitation               | Linux    | x64   | Medium      |
| [Memory](CONFidence%20CTF%202014/Main%20event/Memory)                           | CONFidence CTF 2014          | Reverse Engineering        | Windows  | x86   | Easy        |
| [Multipurpose Calculation Machine](CONFidence%20CTF%202014/Teaser/Multipurpose%20Calculation%20Machine) | CONFidence CTF 2014 (Teaser) | Exploitation               | Linux    | x86   | Medium      |

## Running the tasks

For exploitation problems, if the program listens on a port by default, leave it running and connect to the port to interact with the task. If it reads and writes to/from `stdin` and `stdout`, you should bind it to a TCP port of your choice (e.g. with `netcat` or `socat` on Linux, and the enclosed `AppJailLauncher.exe` tool on Windows), and connect to it to exploit the vulnerabilities.

For reverse-engineering problems, the goal is to extract the flag from the provided executable file.

## About Dragon Sector

![Dragon Sector](logo.png)

Dragon Sector is a Polish security Capture The Flag team. It was created in February 2013 and currently has 17 active members. We frequently participate in both on0line and offline security Capture The Flag competitions, publish write-ups on CTF tasks, and sometimes even organize CTFs.

You can find us on [CTFTime](https://ctftime.org/team/3329), [our blog](https://blog.dragonsector.pl/) and [Twitter](https://twitter.com/DragonSectorCTF).

## Contact

Questions, comments? Let me know at j00ru.vx@gmail.com.
