#AUTHOR : AGASTYA DHAND
import os, pygame, subprocess
from pygame.locals import *

pygame.init()

#window state
state = 'homepage'

#constants
window_width, window_height = 800, 600
option_button_color = (24, 11, 54)
option_hover_color = (86, 23, 117)
game_button_color = (255, 100, 100)
game_hover_color = (255, 150, 150)
font_color = (255, 255, 0)
highlight_font_color = (255, 255, 255)
title_color = (163, 33, 122)

#fonts
TITLE_FONT = pygame.font.Font(pygame.font.match_font("impact"), 80) 
BUTTON_FONT = pygame.font.Font(pygame.font.match_font("consolas"), 28)  

#display setup
DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ARCADE")

#background image
script_dir = os.path.dirname(os.path.abspath(__file__))  #directory of the current script

homepage_bg_image = pygame.image.load(os.path.join(script_dir, "homepage_bg.png"))
homepage_bg_image = pygame.transform.scale(homepage_bg_image, (window_width, window_height))

arcade_bg_image = pygame.image.load(os.path.join(script_dir, "arcade_bg.png"))
arcade_bg_image = pygame.transform.scale(arcade_bg_image, (window_width, window_height))


#button classes
class Button_mainmenu:
    def __init__(self, text, width, height, callback, vertical_offset=0):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.callback = callback
        self.hovered = False
        self.rect.center = (window_width // 2, window_height // 2 + vertical_offset)

    def draw(self, surface):
        color = game_hover_color if self.hovered else game_button_color
        text_color = highlight_font_color if self.hovered else font_color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = BUTTON_FONT.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                self.callback()

class Button_homepage(Button_mainmenu):
    def __init__(self, text, width, height, callback, vertical_offset=0):
        super().__init__(text, width, height, callback, vertical_offset)
        self.rect.center = (window_width // 6, (window_height // 3) + 50 + vertical_offset)
    
    def draw(self, surface):
        color = option_hover_color if self.hovered else option_button_color
        text_color = highlight_font_color if self.hovered else font_color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        text_surf = BUTTON_FONT.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

#callback fns to launch games
def launch_game_1():
    game_path = os.path.join(script_dir, "memorypuzzle.py")
    subprocess.Popen(["python", game_path])

def launch_game_2():
    game_path = os.path.join(script_dir, "slidepuzzle.py")
    subprocess.Popen(["python", game_path])

def launch_game_3():
    game_path = os.path.join(script_dir, "testing.py")
    subprocess.Popen(["python", game_path])

def launch_game_4():
    game_path = os.path.join(script_dir, "wormyyy.py")
    subprocess.Popen(["python", game_path])


def quit_program():
    pygame.quit()
    exit()

def go_to_mainmenu():
    global state
    state = 'mainmenu'

def go_to_homepage():
    global state
    state = 'homepage'

#button instances
homepage_buttons = [
    Button_homepage("PLAY", 200, 50, go_to_mainmenu, vertical_offset=0),
    Button_homepage("QUIT", 200, 50, quit_program, vertical_offset=80),
]

mainmenu_buttons = [
    Button_mainmenu("Memory Match", 300, 50, launch_game_1, vertical_offset=0),
    Button_mainmenu("15 Slide Puzzle", 300, 50, launch_game_2, vertical_offset=60),
    Button_mainmenu("Simulate", 300, 50, launch_game_3, vertical_offset=120),
    Button_mainmenu("Wormy", 300, 50, launch_game_4, vertical_offset=180),
    Button_mainmenu("BACK", 200, 50, go_to_homepage, vertical_offset=260),
]

#main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit_program()

        if state == "homepage":
            for button in homepage_buttons:
                button.handle_event(event)
        elif state == "main_menu":
            for button in mainmenu_buttons:
                button.handle_event(event)

    if state == "homepage":
        pygame.display.set_caption("ARCADE")
        DISPLAYSURF.blit(homepage_bg_image, (0, 0))
        title_surf = TITLE_FONT.render("Welcome to the Arcade!", True, title_color)
        title_rect = title_surf.get_rect(center=(window_width // 2, 85))
        DISPLAYSURF.blit(title_surf, title_rect)
        for button in homepage_buttons:
            button.draw(DISPLAYSURF)

    elif state == "mainmenu":
        pygame.display.set_caption("GAME MENU")
        DISPLAYSURF.blit(arcade_bg_image, (0, 0))

        #drawing title
        title_surf = TITLE_FONT.render("Select a game to Play!", True, font_color)
        title_rect = title_surf.get_rect(center=(window_width // 2, 85))
        DISPLAYSURF.blit(title_surf, title_rect)

        #event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_program()
            for button in mainmenu_buttons:
                button.handle_event(event)

        #adding buttons
        for button in mainmenu_buttons:
            button.draw(DISPLAYSURF)

    pygame.display.update()