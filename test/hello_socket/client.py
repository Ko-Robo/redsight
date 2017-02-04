import sys
import socket



argvs = sys.argv

if len(argvs) != 3:
  print("Invalid Argument.")
  print("useage: $ python clinet.py addr port")

serverAddr = argvs[1]
serverPort = int(argvs[2])

client_sock = socket.socket()
client_sock.connect((serverAddr, serverPort))
client_sock.send(b"hello")
data=client_sock.recv(1024)
print(data)
client_sock.close()
