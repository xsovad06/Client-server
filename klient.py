#!/usr/bin/env python3

from socket import *

message = b"www.fit.vutbr.cz:A\nwww.google.com:A\nwww.brno.cz:A\nwww.facebook.com:A\n34.213.147.57:PTR\n147.229.2.90:PTR"
message2 = b"www.fit.vutbr.cz:PTR\nwww.google.com:A\nwww.brno.cz:A\nwww.wikipedia.com:A\n34.213.147.57:A\n147.229.2.90:PTR"
message3= b"www.testofnonexistingdomainname.czek:A\nwww.testofanothernonexistingdomainname.skek:A"

PORT = 6543       # The port used by the server
message = b"www.fit.vutbr.cz:A\nwww.google.com:A\nwww.brno.cz:A\nwww.stackoverflow.com:A\n34.213.147.57:PTR\n147.229.2.90:PTR"

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(('', PORT))
    s.sendall(b"POST /dns-query HTTP/1.1\r\n" + message)
    data = s.recv(1024)

print('Received', repr(data))
