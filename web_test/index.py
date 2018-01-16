#!/usr/bin/python
# -*- coding: utf-8 -*

import cgi
import socket

hotsname=socket.gethostname()
ip=socket.gethostbyname(socket.gethostname())

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

html = """<!DOCTYPE html>
<head>
    <title>Test_front</title>
</head>
<body>
    <h1>Test page</h1>
    <h2>Hostname :</h2>
    """ + hotsname + """
    <h2>IP :</h2>
    """ + ip + """
</body>
</html>
"""

print(html)
