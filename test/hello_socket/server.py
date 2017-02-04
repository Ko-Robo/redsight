import socket


class HelloServer:
  def __init__(self, addr, port):
    self.server_sock = socket.socket()
    self.server_sock.bind((addr, port))

    self.server_sock.listen(1)

    print(self.server_sock)

  def start(self):
    conn, addr = self.server_sock.accept()

    print("connect by ", str(addr))
    conn.send(b"hello")
    conn.close()

server = HelloServer("localhost", 4003)
server.start()
