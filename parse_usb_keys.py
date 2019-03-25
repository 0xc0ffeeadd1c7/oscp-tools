#!/usr/bin/python
#https://wiki.wireshark.org/USB
#https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
#Mapping is incomplete - refer to above reference to add further
#In some cases this script will output a shift-hold as two PostFails and shift-release as a single PostFail

import sys

mapping = {
	2:"PostFail",
	4:"a",
	5:"b",
	6:"c",
	7:"d",
	8:"e",
	9:"f",
	10:"g",
	11:"h",
	12:"i",
	13:"j",
	14:"k",
	15:"l",
	16:"m",
	17:"n",
	18:"o",
	19:"p",
	20:"q",
	21:"r",
	22:"s",
	23:"t",
	24:"u",
	25:"v",
	26:"w",
	27:"x",
	28:"y",
	29:"z",
	30:"1",
	31:"2",
	32:"3",
	33:"4",
	34:"5",
	35:"6",
	36:"7",
	37:"8",
	38:"9",
	39:"0",
	40:"Enter",
	41:"esc",
	42:"del",
	43:"tab",
	44:"space",
	45:"-",
	47:"[",
	48:"]",
	52:"'",
	55:".",
	56:"/",
	57:"CapsLock",
	79:"RightArrow",
	80:"LeftArrow",
	184:"{",
	185:"}",
	187:"Backspace",
	225:"LeftShift",
	229:"RightShift"
}

def usage():
  print "%s <usb-key-hex-file>" % sys.argv[0]

def main():
  if len(sys.argv) != 2:
    usage()
  else:
    #This script is intended to read a .csv with hex values of Leftover Capture data as hex
    with open(sys.argv[1], 'rb') as f:
      for line in f.readlines():
        #mostly just to skip the first line if the column was exported from Wireshark
        if not "Leftover Capture Data\n" in line:
          #Strip out each line into bytes and store in an array
          bytes = bytearray.fromhex(line.strip())
          #iterate over each byte within a line and map it to USB HID table
          for byte in bytes:            
	    if byte != 0:
              if int(byte) in mapping.keys():
                print mapping.get(int(byte))
              else: 
		print byte

main()
