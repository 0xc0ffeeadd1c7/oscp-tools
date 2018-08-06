#!/usr/bin/python

import subprocess as sub
import os
import sys

def usage():
  print "Nmap Vulnerability scanning tool - Usage:\n"
  print "nmap-vuln.py <ip-address> <port> <service>"

def main():
  print "[*] Starting nmap scan against %s on port %s for %s vulnerabilities\n" %(sys.argv[1], sys.argv[2], sys.argv[3])
  ip = sys.argv[1]
  port = sys.argv[2]
  script_name = sys.argv[3]
  scripts = []
  for script in os.listdir("/usr/share/nmap/scripts/"):
    if script_name in script:
        scripts.append(script)
    else: continue
  for script in scripts:
    print "[*] Scanning for %s " %script
    command = sub.Popen(['nmap', '-p ' + port, '--script='+script, ip], stdout=sub.PIPE) 
    output = command.communicate()[0]
    print output

if len(sys.argv) != 4:
  usage()
else:
  main()
