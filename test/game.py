
import sys

import pygame 



from game_screen import *
from io_item import *
from client import *

######


class Game():
  def __init__(self, server_addr="", server_port=0):
    self.dict = {}
    
    self.client = Client(server_addr=server_addr, server_port=server_port)
    self.dict['client'] = self.client

    self.io_item = IOItem()
    self.dict['io_items'] = self.io_item
    
    self.game_screen = GameScreen()
    self.dict['screen'] = self.game_screen
    
    self.client_params_string = ""
    self.dict['client_params_string'] = self.client_params_string
    

  def run_game(self):
    # error
    if not self.client.sock_built :
      print("socket is not built")
      return

    # loop
    while(1):
      # client 
      str = self.client.update(self.dict)

      self.game_screen.update(self.dict)

      
      

def main(server_addr="", server_port=0):
  game = Game(server_addr = server_addr, server_port=server_port)
  game.client.connect_to_server()
  game.run_game()


if __name__ == "__main__":

  argvs = sys.argv
  if len(argvs) != 3:
    print("Invalid Argument.")
    print("useage: $ python game.py addr port")
    sys.exit()

  serverAddr = argvs[1]
  serverPort = int(argvs[2])

  main(server_addr = serverAddr, server_port=serverPort)
