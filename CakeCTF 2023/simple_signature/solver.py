import socket
import re
import os
import sys
from hashlib import sha512
from Crypto.Util.number import getRandomRange, getStrongPrime, inverse, GCD
import signal

HOST = "crypto.2023.cakectf.com"
PORT = 10444

p, g, vkey = 0, 0, (0, 0)

def find_y(p, w, v):
    y = pow(w, -1, p-1) * v % (p-1)
    return y

def sign(m, key):
    x, y, u = key
    r = getRandomRange(2, p-1)
    return pow(g, x*m + r*y, p), pow(g, u*m + r, p)

def h(m):
    return int(sha512(m.encode()).hexdigest(), 16)

with socket.create_connection((HOST, PORT)) as socket:
    # Receive and print the initial data
    data = socket.recv(4096).decode()

    numbers = re.findall(r'\d+', data)
    p, g, *vkey = (int(num) for num in numbers)

    y = find_y(p, *vkey)

    # Send the 'V' option
    socket.sendall(b'V\n')

    socket.recv(4096).decode()

    # Send the message for verification
    message = "cake_does_not_eat_cat"
    socket.sendall(f"{message}\n".encode())

    socket.recv(4096).decode()

    w, v = vkey
    x = getRandomRange(2, p-1)
    u = (w * x - 1) * inverse(v, p-1) % (p-1)

    s, t = sign(h(message), (x, y, u))

    socket.sendall(f'{s}\n'.encode())
    socket.recv(4096).decode()
    socket.sendall(f'{t}\n'.encode())

    # extract flag
    response = socket.recv(4096).decode()
    flag = re.search(r'flag = (.*)', response).group(1)
    print(flag)


