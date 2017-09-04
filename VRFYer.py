#!/usr/bin/env python2
'''
    Bruteforces the SMTP VRFY command to check for existing accounts on the server

    Any comments or questions can be sent to _@sp2.io <Yoram van de Velde>
'''

import socket
import sys

if len(sys.argv) <= 2:
	print "Usage: vrfy.py <server> [username file]"
	sys.exit(0)

if len(sys.argv) == 3:
        try:
		f = open(sys.argv[2], 'r')
	except:
		print "Failed to open username file."
		sys.exit(1)
else:
	f = [
		'root', 'admin', 'test', 'guest',
		'info', 'adm', 'mysql', 'user',
		'administrator', 'oracle', 'ftp'
	]

server = sys.argv[1]

# Setup connection and print banner.
print "Connecting to %s" % server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con = s.connect((server, 25))
print s.recv(1024)

# Some servers want to meet and greet first
s.send("HELO google.com\r\n")
print s.recv(1024)

# Test for VRFY
print "Testing for VRFY"
s.send('VRFY testuser\r\n')
testresult = s.recv(1024).split()

# The test returns one of these statusses most likely
# 250 = ok
# 252 = cannot verify, but will try to deliver
# 501 = syntax error, might miss domainname
# 502 = not implemented

if testresult[0] == '502':
    print "%s does not support VRFY\nExiting. Bye.\n" % server
    sys.exit(-1)
else:
    print "%s seems to support VRFY...\n" % server

# Connected and VRFY seems to work. Lets bruteforce some users
for user in f:
    print "Sending VRFY %s" % user.strip()
    s.send('VRFY ' + user.strip() + '\r\n')
    result = s.recv(1024)
    print result.strip()

# Done with list... Close connection
print "Closing connection to %s\n\n" % server
s.close()

