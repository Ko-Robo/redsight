
import socket
from time import sleep
from io_item import * 


### server

class RaspiServer:
  def __init__(self, addr, port):
    self.server_sock = socket.socket()
    self.server_sock.bind((addr, port))
    self.server_sock.listen(1)

    self.io_item = IOItem()

  
  def str_to_values(self, str):
    pass

  def start(self):
    conn, addr = self.server_sock.accept()

    try :

      print("connected by ", addr)

      while(1):      
        conn.send((self.io_item.make_io_string()).encode("utf-8"))
        got_data = conn.recv(4096).decode('ascii')


        item_list = parse_string(got_data)
        list(map(lambda item : self.io_item.update_item(item[0], item[1]),
                 item_list))


        sleep(0.1)


      
    except BrokenPipeError:
      print("pipe was broken")
      self.start()

    except ConnectionResetError:
      print("connection reset ")
      self.start()
      

    conn.close()


server = RaspiServer("localhost", 4003)
server.start()

