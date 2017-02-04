import sys
import socket

from io_item import *

class Client():
  def __init__(self, server_addr="", server_port=0):
    
    self.server_addr = server_addr
    self.server_port = server_port
    self.sock = socket.socket()
    self.sock_built = False

  def connect_to_server(self):
    try :
      self.sock.connect((self.server_addr, self.server_port))
      self.sock_built = True
      
    except ConnectionRefusedError:
      print("connection refused")


  def recv(self):
    str = self.sock.recv(2048)
    #print(str)
    return str


  def send_data(self, dict):
    self.sock.send((dict['client_params_string'] + " ").encode())
    
  
  def update(self, dict):
    got_str = self.recv().decode("utf-8")

    self.send_data(dict)

    item_list = parse_string(got_str)
    list(map(lambda item : dict['io_items'].update_item(item[0], item[1]) ,
             item_list))

    return got_str


