import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("server_public_ip", 12345))

file = open("recieved.jpg", "wb")
data = None
while True:
    m = sock.recv(1024)
    data = m
    if m:
        while m:
            m = sock.recv(1024)
            data += m
        else:
            break
file.write(data)
file.close()
print("Done receiving")
