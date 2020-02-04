#!/usr/bin/python3
'''
This script is intended for converting signed or unsigned integer arrays (such as those found in malicious .hta or vbscript files) to shellcode in binary format for further analysis.

Based off 0xdf's blog post (https://0xdf.gitlab.io/2018/11/13/malware-analysis-phishing-docs-from-htb-reel.html) and my own analysis of shellcode from malicious vbscript/.hta files. such as those generated with msfvenom.

The script takes a the input file name as its first argument and an output file name as its second parameter. The input file should only contain comma-separated signed integer values.

python3 int2shellcode.py <input file> <output file>

========== Example input file contents ==========
-123,-80,-4,-128,-43,27,-96,36,-99,-79,-75,84,-4,-35,122,85,-1,29,21,-18,-116,47,-70,68,27,3,51,67,-36,100,110,51,114,-101,-111,68,90,95,-59,20,-12,118,102,-1,4,119,-77,80,85,-41,108,17,5,-105,-36,-7,79,24,2,25,112,-13,43,50,-88,-5,83,-61,-46,-115,58,-81,49,21,-46,66,43,-68,66,-77,-59,81,-76,-125,77,-17,-79,116,94,-80,2,72,-22,17,-7,-58,33,-14,113,127,119,127,26,76,37,2,-38,-38,96,-44,-18,-102,-116,-15,-124,-37,110,-109,-112,-117,-26,97,-91,42,76,-20,67,70,-94,-72,-36,-1,91,-31,-105,-98,-92,60,-46,-95,47,-76,34,111,-40,-67,48,-104,-65,61,-55,89,42,61,-93,93,-4,106,91,92,-39,92,-60,-97,12,-33,3,95,-47,-23
==========              EoF            ==========
'''
import sys

inputFile = ""

with open(sys.argv[1], 'r') as f:
  inputFile = f.read()
f.close()

stringArray = inputFile.split(',')

intArray = [int(i) & (2**8-1) for i in stringArray]

shellcode = ""
byteArray = []

for i in intArray:
  byte = hex(i)[2:]
  if len(byte) < 2:
    byte = '0' + byte
  shellcode += byte

with open(sys.argv[2], 'wb') as f:
  f.write(bytearray(shellcode, 'utf-8'))

f.close()
