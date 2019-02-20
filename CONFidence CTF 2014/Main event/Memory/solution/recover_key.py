#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename:         recover_key.py
# Author:           Mateusz Jurczyk
# Task:             Memory
# Competition:      CONFidence CTF 2014
# Category:         Reverse engineering
# Scoring:          50 pts (easy)
# Number of solves: 2 out of 11 participants

__author__ = "Mateusz Jurczyk"
__copyright__ = "Copyright 2014, Mateusz Jurczyk"
__license__ = "Apache"
__version__ = "2.0"

import struct

def Handler_Add(buffer, idx, arg):
  buffer[idx] = (buffer[idx] + arg) & 0xff
  return False

def Handler_Sub(buffer, idx, arg):
  buffer[idx] = (buffer[idx] - arg) & 0xff
  return False

def Handler_Xor(buffer, idx, arg):
  buffer[idx] = (buffer[idx] ^ arg) & 0xff
  return False

def Handler_Not(buffer, idx, arg):
  buffer[idx] = (~buffer[idx]) & 0xff
  return False

def Handler_Cmp(buffer, idx, arg):
  return False

def Handler_Exit(buffer, idx, arg):
  return True

def RunVM(program, buffer):
  for offset in xrange(0, len(program), 8):
    op = struct.unpack("<I", program[offset: offset + 4])[0]
    idx = ord(program[offset + 4])
    arg = ord(program[offset + 5])

    handlers = {
      0 : Handler_Add,
      1 : Handler_Sub,
      2 : Handler_Xor,
      3 : Handler_Not,
      4 : Handler_Cmp,
      5 : Handler_Exit
    }

    if handlers[op](buffer, idx, arg):
      break

def main():
  EXPECTED_BUFFER = [0xd4, 0x00, 0xee, 0x9a, 0xac,
                     0xbc, 0x93, 0x87, 0x69, 0x96,
                     0x91, 0x59, 0x9b, 0xb5, 0x1e,
                     0x44, 0xe7, 0x2e, 0x64, 0xef]
  key = ['_'] * 20

  print "".join(key)

  with open("unpacked.exe", "rb") as f:
    file_data = f.read()

  for c in xrange(0x20, 0x7f):
    buffer = [c] * 20
    RunVM(file_data[0x1440:], buffer)

    key_updated = False
    for i in xrange(20):
      if buffer[i] == EXPECTED_BUFFER[i]:
        key[i] = chr(c)
        key_updated = True

    if key_updated:
      print "".join(key)

if __name__ == "__main__":
  main()
