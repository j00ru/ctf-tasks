#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename:         disasm.py
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

def Disassemble(program):
  for offset in xrange(0, len(program), 8):
    op = struct.unpack("<I", program[offset: offset + 4])[0]
    op = ["add", "sub", "xor", "neg", "cmp", "exit"][op]
    idx = ord(program[offset + 4])
    arg = ord(program[offset + 5])
    
    if op == "exit":
      print "[%.8x] exit" % (offset)
      break
    elif op == "neg":
      print "[%.8x] neg [%2d]" % (offset, idx)
    else:
      print "[%.8x] %s [%2d], 0x%x" % (offset, op, idx, arg)

def main():
  with open("unpacked.exe", "rb") as f:
    file_data = f.read()

  Disassemble(file_data[0x1440:])

if __name__ == "__main__":
  main()
