import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 12345))
sock.listen(10)
connection, addr = sock.accept()
print('{} connected.'.format(addr))
file = open("image.jpg", "rb")
length = os.path.getsize("image.jpg")
m = file.read(l)
connection.send_all(m)
file.close()
print("Done sending")
