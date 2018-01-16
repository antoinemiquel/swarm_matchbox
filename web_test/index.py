#!/usr/bin/python
# -*- coding: utf-8 -*

import cgi
import socket

hostname=socket.gethostname()
#ip=socket.gethostbyname(hostname)

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

html = """<!DOCTYPE html>
<head>
    <title>Test_front</title>
</head>
<body>
    <h1>Test page</h1>
    <h2>Hostname : """ + hostname + """</h2>
</body>
</html>
"""

print(html)
