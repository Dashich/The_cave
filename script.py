import pygame
import os
import script1
import ptext
import sys

class TextButton(pygame.sprite.Sprite):
    def __init__(self, group, poit_pos, size):
        super().__init__(group)
        self.event = None
        self.rect = pygame.Rect(poit_pos, size)
        self.font = pygame.font.SysFont(None, 24)
        self.image = self.font.render("", 1, (255, 255, 255))
        self.layer = 1
    
    def set_text(self, text):
        self.image, pos = ptext.draw(text, (900, 0), color=('#4d4d4d'))
    
    def set_event(self, event):
        self.event = event
    
    def update(self, pos, click):
        if self.check_pos(pos):
            if self.event != None and click:
                self.event()
    
    def check_pos(self, mouse_pos):
        x, y = mouse_pos
        return (self.rect.x <= x and x <= self.rect.x + self.rect.width) and (self.rect.y <= y and y <= self.rect.y + self.rect.height)
    
    
class TextFrame(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        fullname = os.path.join('data', 'interfase', 'text_box.png')
        self.image = pygame.image.load(fullname).convert()
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 482 
        self.layer = 0


class Button(pygame.sprite.Sprite):
    def __init__(self, group, point_pos, folder_name, group_name, is_disable=False):
        super().__init__(group)
        self.is_disable = is_disable
        x, y = point_pos
        self.group_name = group_name
        self.event = None
        self.normal = self.load_image(folder_name, group_name + '_normal.png')
        self.image = self.normal
        self.active = self.load_image(folder_name, group_name + '_active.png')
        if os.path.exists(os.path.join('data', folder_name, group_name + '_disable.png')):
            self.disable = self.load_image(folder_name, group_name + '_disable.png')
        self.rect = self.normal.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def check_pos(self, mouse_pos):
        x, y = mouse_pos
        return (self.rect.x <= x and x <= self.rect.x + self.rect.width) and (self.rect.y <= y and y <= self.rect.y + self.rect.height)
    
    def set_event(self, procedure):
        self.event = procedure
    
    def update(self, mouse_pos, click):
        if self.is_disable:
            return
        if self.check_pos(mouse_pos):
            self.image = self.active
            if self.event != None:
                if click:
                    self.event(self.group_name)
        else:
            self.image = self.normal
    
    def change_disable(self, is_disable):
        self.is_disable = is_disable
        if self.is_disable:
            self.image = self.disable
        else:
            self.image = self.normal
        
    def load_image(self, folder_name, name, colorkey=None):
        fullname = os.path.join('data', folder_name, name)
        image = pygame.image.load(fullname).convert_alpha()
        return image
    
    
class Indicator(pygame.sprite.Sprite):
    def __init__(self, group, point_pos):
        super().__init__(group)
        x, y = point_pos
        self.on = self.load_image('interfase', 'on.png')
        self.image = self.on
        self.off = self.load_image('interfase', 'off.png')
        self.rect = self.on.get_rect()
        pygame.mixer.music.load('data/sounds/sound.ogg')
        self.rect.x = x
        self.rect.y = y
        
    def set_on(self, is_on):
        if is_on:
            self.image = self.on
            pygame.mixer.music.play(-1)
        else:
            self.image = self.off
            pygame.mixer.music.stop()
            
    def load_image(self, folder_name, name, colorkey=None):
        fullname = os.path.join('data', folder_name, name)
        image = pygame.image.load(fullname).convert_alpha()
        return image    
    
    
pygame.init()

def click(group_name):
    global current_room
    steps = pygame.mixer.Sound('data/sounds/steps.ogg')
    if group_name == 'right_arrow':
        current_room = new_room(current_room.r_room_id)
    elif group_name == 'down_arrow':
        current_room = new_room(current_room.back_room_id)
    elif group_name == 'left_arrow':
        current_room = new_room(current_room.l_room_id)
    elif group_name == 'up_arrow':
        current_room = new_room(current_room.fwd_room_id)
    if sound_on:
        steps.play()
    
def new_room(room_id):
    room = data_base.get_room(room_id)
    up_btn.change_disable(room.fwd_room_id == None)
    down_btn.change_disable(room.back_room_id == None)
    left_btn.change_disable(room.l_room_id == None)
    right_btn.change_disable(room.r_room_id == None)
    background_image = pygame.image.load(os.path.join('data', 'background', room.background)).convert()
    screen.blit(background_image, [0, 0])
    text_lable.set_text(room.get_description())
    return room

def text_click():
    text = current_room.get_description()
    if text != '':
        text_lable.set_text(text)
        
def exit(group_name):
    pygame.quit()
    sys.exit()

def main_menu(gr_name):
    def play_click(group_name):
        nonlocal running_menu
        global current_room
        running_menu = False
        if 'current_room' in globals():
            background_image = pygame.image.load(os.path.join('data', 'background', current_room.background)).convert()
            screen.blit(background_image, [0, 0])  
            sound_btn.kill()
            sound_ind.kill()
            play_btn.kill()
            exit_btn.kill()
            help_btn.kill()
            if current_room.get_game_over():
                current_room = new_room(1)
    def help(group_name):
        background_help = pygame.image.load(os.path.join('data', 'background', 'help.png')).convert()
        screen.blit(background_help, [0, 0])
        pygame.display.flip()
        running_help = True
        while running_help: 
            for event in pygame.event.get():
                running_help = not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
        screen.blit(background_image, [0, 0])
        menu.draw(screen)
        pygame.display.flip()       
    def sound(group_name):
        global sound_on
        sound_on = not sound_on
        sound_ind.set_on(sound_on)
    menu = pygame.sprite.Group()
    play_btn = Button(menu, (34, 87), 'interfase', 'play')
    play_btn.set_event(play_click)
    sound_btn = Button(menu, (34, 191), 'interfase', 'options')
    sound_ind = Indicator(menu, (190, 235))
    sound_ind.set_on(sound_on)
    sound_btn.set_event(sound)
    help_btn = Button(menu, (34, 295), 'interfase', 'help')
    help_btn.set_event(help)
    exit_btn = Button(menu, (34, 399), 'interfase', 'exit')
    exit_btn.set_event(exit)
    background_image = pygame.image.load(os.path.join('data', 'background', 'menu.png')).convert()
    screen.blit(background_image, [0, 0])
    menu.draw(screen)
    pygame.display.flip()
    running_menu = True
    while running_menu: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                menu.update(event.pos, event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
                menu.draw(screen)
                pygame.display.flip()
    

sound_on = True
data_base = script1.DataBase('game_data.db')
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('The Cave')
main_menu('')
sprites = pygame.sprite.Group()
right_btn = Button(sprites, (748, 541), 'interfase', 'right_arrow')
right_btn.set_event(click)
down_btn = Button(sprites, (696, 541), 'interfase', 'down_arrow')
down_btn.set_event(click)
left_btn = Button(sprites, (644, 541), 'interfase', 'left_arrow')
left_btn.set_event(click)
up_btn = Button(sprites, (696, 482), 'interfase', 'up_arrow')
up_btn.set_event(click)
menu_btn = Button(sprites, (5, 5), 'interfase', 'menu')
menu_btn.set_event(main_menu)
text_box = TextFrame(sprites)
text_lable = TextButton(sprites, (12, 489), (627, 96))
text_lable.set_text('')
text_lable.set_event(text_click)
current_room = new_room(1)
sprites.draw(screen)
pygame.display.flip()
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            sprites.update(event.pos, event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            sprites.draw(screen)
            pygame.display.flip()
pygame.quit()