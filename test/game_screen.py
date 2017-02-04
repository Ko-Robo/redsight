
import pygame 
from pygame.locals import *
from copy import copy

import sys

from io_item import *


### constants
color_black = (0,0,0)
color_white = (255,255,255)
color_blue = (0,0,255)

FONT_SIZE = 18
RECT_SIZE = 18

### core object
 
class Object:
  def __init__(self, dict):
    pass
  def update(self, dict):
    pass        


    
class Splite(Object):
  # x, y : center of characters
  def __init__(self, dict, color=(0,0,0), x=0, y=0):
    self.color = color
    self.x, self.y = x, y

    self.width = CHARACTER_WIDTH
    self.half_width = self.width/2



  def draw(self, dict):
    pygame.draw.rect(dict['screen'], self.color,
                     Rect(self.x-self.half_width, self.y-self.half_width,
                          self.width, self.width))
    
  def change_width(self, width):
    width = round(width)
    if width%2 == 1 :
      width -= 1
    self.width = width
    self.half_width = width/2

  def rect(self):
    return Rect(self.x-self.half_width, self.y-self.half_width, self.width, self.width)

  def rect_when_xy(self, x, y):
    return Rect(x-self.half_width, y-self.half_width, self.width, self.width)
  
  def collision(self, splite):
    self_rect = self.rect()
    splite_rect = splite.rect()
    
    return self_rect.colliderect(splite_rect)


### key event 
class SystemEvent(Object):
  def update(self, dict):
    # key board
    for event in dict['event']:
      if event.type == QUIT: sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE: sys.exit()
        if event.key == K_d: sys.exit()





### Parameter Area
class ParamArea(Object):
  # to show many parameter of game
  
  def __init__(self, dict):
    # df : default font
    self.char_width = 18
    self.df = pygame.font.SysFont(None, self.char_width)
    self.line_length = 30
    self.text_list = []
    
    self.fps = None

  def text_render(self, text):
    return self.df.render(text, True, color_black)

  def update_text_list(self, text_list):
    return list(map(lambda text: self.text_render(text[0:self.line_length]),
                    text_list))
  def draw_text_list (self, screen, text_list, x=0, y=0):
    pygame.draw.rect(screen, (0,0,255), Rect(x-5,y-5,
                                             self.line_length*self.char_width*0.4+5,
                                             self.line_length*len(text_list)*0.7+5),
                     2)
    for i in range(len(text_list)):
      screen.blit(text_list[i], (x, y+i*self.char_width))
    
  def update(self, dict, game_dict):
    items = dict['io_items']
    
    items_string_list = items.make_item_string_list()

    ### text_list1
    self.text_list1 = self.update_text_list(
      ["game params",
       "fps : " + str(game_dict['fps'])]
      + items_string_list[:21])

    self.text_list2 = self.update_text_list(
      items_string_list[21:])
    
  def draw(self, dict):
    screen = dict['screen']
    self.draw_text_list(screen, self.text_list1, x=20, y=20)
    self.draw_text_list(screen, self.text_list2, x=300, y=20)


### enegy rect
class EnegyRect(Splite):
  # |++++++++------------| 
  # -> 8/20 = 40%
  def __init__(self, dict,x, y, text,width):
    self.x, self.y = x, y

    self.width = width
    self.height = RECT_SIZE

    self.df = pygame.font.SysFont(None, FONT_SIZE)
    self.text = text

    self.percentage = 0.5
    
  def update(self, dict):
    mouse_rect = Rect(dict['mouse_x'], dict['mouse_y'], 1,1)
    rect = Rect(self.x, self.y, self.width, self.height)
    if rect.colliderect(mouse_rect) and dict['mouse_button_down']:
      self.percentage = (dict['mouse_x'] - self.x ) / self.width


  def draw(self, dict):
    pygame.draw.rect(dict['screen'], color_blue,
                     Rect(self.x, self.y, self.width*self.percentage, self.height))
    pygame.draw.rect(dict['screen'], color_black,
                     Rect(self.x, self.y, self.width, self.height) ,
                     1)
    dict['screen'].blit(self.df.render(self.text, True, color_black)
                        , (self.x + self.width+5, self.y))

class Button (Splite):
  def __init__ (self, dict, x, y, text, width):
    self.x = x
    self.y = y

    self.text = text
    
    self.height = RECT_SIZE
    self.width = width

    self.pressing = False
    self.clicked = False
    self.pressed_frame = 0

    self.df = pygame.font.SysFont(None, FONT_SIZE)

  def update(self, dict):
    mouse_rect = Rect(dict['mouse_x'], dict['mouse_y'], 1,1)
    rect = Rect(self.x, self.y, self.width, self.height)
    
    self.clicked = False 

    if rect.colliderect(mouse_rect) and dict['mouse_button_down']:
      self.pressing = True 
      self.clicked = True if self.pressed_frame == 0 else False 
      self.pressed_frame += 1
      
    else :
      self.pressing = False
      self.pressed_frame = 0

  def draw(self, dict):
    pygame.draw.rect(dict['screen'], color_blue,
                     Rect(self.x, self.y, self.width, self.height),
                     False if self.pressing else 1)
    dict['screen'].blit(self.df.render(self.text, True, color_black), 
                        (self.x + self.width+5, self.y))

    
def game_client_params_string(dict, game_dict):
  name_list = [
    "motor1_teach", "motor2_teach", "motor3_teach",
    "teach", "save"]

  value_list = [
    game_dict['motor1_rect'].percentage*2-1,
    game_dict['motor2_rect'].percentage*2-1,
    game_dict['motor3_rect'].percentage*2-1,
    1 if game_dict['teach_button'].pressing else 0,
    1 if game_dict['save_button'].clicked else 0
  ]

  str = items_to_string(name_list, value_list)

  return str
    


### screen

class GameScreen():
  def __init__ (self):
    self.game_dict = {}
        
    # base
    pygame.init()
    self.game_dict['screen']=pygame.display.set_mode((640, 600))
    pygame.display.set_caption(u"sample game")

    # clock
    clock = pygame.time.Clock()
    self.game_dict['clock'] = clock

    self.game_dict['frame_start'] = pygame.time.get_ticks()
    self.game_dict['frame_end'] = pygame.time.get_ticks()
    self.game_dict['fps'] = 0

    # key, mouse event
    self.game_dict['system_event'] = SystemEvent(self.game_dict)
    self.game_dict['mouse_x'] =0
    self.game_dict['mouse_y'] =0
    self.game_dict['mouse_button_down'] =0
    

    # user

    self.param_area = ParamArea(self.game_dict)
    self.game_dict['param_area'] = self.param_area


    # params to tearch



    self.motor1_rect = EnegyRect(self.game_dict, 20, 500, "motor1", 100)
    self.game_dict['motor1_rect'] = self.motor1_rect

    self.motor2_rect = EnegyRect(self.game_dict, 20, 520, "motor2", 100)
    self.game_dict['motor2_rect'] = self.motor2_rect

    self.motor3_rect = EnegyRect(self.game_dict, 20, 540, "motor3", 100)
    self.game_dict['motor3_rect'] = self.motor3_rect


    self.teach_button = Button(self.game_dict, 20, 560, "teach", 100)
    self.game_dict['teach_button'] = self.teach_button

    self.save_button = Button(self.game_dict, 20, 580, "save", 200)
    self.game_dict['save_button'] = self.save_button
    
    
    
  def update(self, dict):
    # key event
    x,y=pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed()[0]
    self.game_dict['mouse_x'] =x
    self.game_dict['mouse_y'] =y
    self.game_dict['mouse_button_down'] =mouse_button

    self.game_dict['event'] = copy(pygame.event.get())
    self.game_dict['event_pressed'] = copy(pygame.key.get_pressed())

    self.game_dict['system_event'].update(self.game_dict)


    # fps update
    self.game_dict['frame_end'] = pygame.time.get_ticks()
    self.game_dict['clock'].tick()
    self.game_dict['frame_start'] = pygame.time.get_ticks() 
    self.game_dict['fps'] = self.game_dict['clock'].get_fps()


    # parameter area
    self.game_dict['param_area'].update(dict, self.game_dict)

    self.game_dict['motor1_rect'].update(self.game_dict)
    self.game_dict['motor2_rect'].update(self.game_dict)
    self.game_dict['motor3_rect'].update(self.game_dict)

    self.game_dict['teach_button'].update(self.game_dict)
    self.game_dict['save_button'].update(self.game_dict)

    # draw to screen
    pygame.draw.rect(self.game_dict['screen'], (255,255,255), Rect(0,0,640,600))
    self.game_dict['param_area'].draw(self.game_dict)

    self.game_dict['motor1_rect'].draw(self.game_dict)
    self.game_dict['motor2_rect'].draw(self.game_dict)
    self.game_dict['motor3_rect'].draw(self.game_dict)

    self.game_dict['teach_button'].draw(self.game_dict)
    self.game_dict['save_button'].draw(self.game_dict)


    # display update
    pygame.display.update()

    # make string to report to server
    dict['client_params_string'] = game_client_params_string(dict, self.game_dict)
