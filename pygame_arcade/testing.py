import random, sys, time, pygame
from pygame.locals import *

# SETTING UP BASIC PARAMETERS
fps = 30
width_window = 640
height_window = 640
flashspeed = 1000  # HOW QUICKLY BUTTON LIGHTS UP AND FADES DOWN IN MILLI SEC
flashdelay = 500  # DELAY BETWEEN TWO BUTTON FLASHING IN MILLI SEC
buttonsize = 200  # THE SIDE OF SQUARE BUTTON IN PIXEL
size_between_buttons = 20  # IN PIXEL
timeout = 8  # seconds before game over if no button is pushed

# SETTING UP COLOURS. Bright for light ups
white = (255, 255, 255)
black = (0, 0, 0)
bright_red = (255, 0, 0)
red = (155, 0, 0)
bright_green = (0, 255, 0)
green = (0, 155, 0)
bright_blue = (0, 0, 255)
blue = (0, 0, 155)
bright_yellow = (255, 255, 0)
yellow = (155, 155, 0)
gray = (40, 40, 40)
bgcolour = (150, 150, 150)

# SETTING UP MARGINS
x_margin = int((width_window - 2 * buttonsize - size_between_buttons) / 2)
y_margin = int((height_window - 2 * buttonsize - size_between_buttons) / 2)

# SETTING UP BUTTONS
yellow_button = pygame.Rect(x_margin, y_margin, buttonsize, buttonsize)
blue_button = pygame.Rect(x_margin + buttonsize + size_between_buttons, y_margin, buttonsize, buttonsize)
red_button = pygame.Rect(x_margin, y_margin + buttonsize + size_between_buttons, buttonsize, buttonsize)
green_button = pygame.Rect(x_margin + buttonsize + size_between_buttons, y_margin + buttonsize + size_between_buttons, buttonsize, buttonsize)

# main() function
def main():
    global fps_clock, display_screen, stdfont, bgColor
    pygame.init()  # INITIALIZING MODULE
    fps_clock = pygame.time.Clock()  # creates a Clock object that is used to regulate FPS 
    display_screen = pygame.display.set_mode((width_window, height_window))
    pygame.display.set_caption("SIMULATE GAME")
    stdfont = pygame.font.SysFont("Arial", 18)  # Using SysFont instead of Font
    infoSurf = stdfont.render('Match the pattern by using the Q(yellow), W(BLUE), A(RED), S(GREEN) keys.', 1, gray)
    
    # DEFINING BLOCK OF INFOSURF
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, height_window - 25)
    
    # INITIALIZING IMPORTANT VARIABLES
    pattern = []  # List of colours to be memorised
    currentStep = 0
    lastClickTime = 0
    score = 0
    # when False,the pattern is playing. when True,waiting for the player to click a coloured button
    waitingForInput = False
    bgColor = bgcolour
    
    while True:
        clickedButton = None  # Which button was just clicked
        display_screen.fill(bgColor)  # ADD COLOUR TO BACKGROUND
        drawButtons()

        # SETTING UP SCOREBOARD
        score_screen = stdfont.render("SCORE: " + str(score), 1, white)
        scoreRect = score_screen.get_rect()  # RETURNS A RECTANGLE OBJECT
        scoreRect.topleft = (width_window - 100, 10)  # DEFINES POSITION OF SCOREBOARD
        display_screen.blit(score_screen, scoreRect)  # DRAW ONE SURFACE ON OTHER
        display_screen.blit(infoSurf, infoRect)
        
        # TO CHECK FOR MOUSE CLICKS
        checkForQuit()  # TO CHECK IF USER QUITS
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos  # POSITION OF CLICK
                clickedButton = getButtonClicked(mousex, mousey)

            elif event.type == KEYDOWN:  # CHECKS IF KEYBOARD WAS USED
                if event.key == K_q:
                    clickedButton = yellow  # Q IMPLIES YELLOW
                elif event.key == K_w:
                    clickedButton = blue  # W IMPLIES BLUE
                elif event.key == K_a:
                    clickedButton = red  # A IMPLIES RED
                elif event.key == K_s:
                    clickedButton = green  # S IMPLIES GREEN
        
        if not waitingForInput:
            # GENERATE THE PATTERN
            pygame.display.update()
            pygame.time.wait(1000)  # TIME DELAY OF 1000 MILLI SEC
            pattern.append(random.choice((yellow, blue, red, green)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(flashdelay)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == pattern[currentStep]:
                # CHECKED THAT USED THE CORRECT BUTTON
                flashButtonAnimation(clickedButton)
                currentStep += 1  # GOES TO NEXT STEP
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0  # reset back to first step
            
            # Check for wrong button or timeout
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - timeout > lastClickTime):
                # PLAYER LOST THE GAME
                gameOverAnimation()
                # RESET:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
                
        pygame.display.update()  # COMMIT CHANGES TO DISPLAY
        fps_clock.tick(fps) 

def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()

# TO CREAT FLASHING ANIMATION BY CHANGING COLOUR
def flashButtonAnimation(color, animationSpeed=50):
    if color == yellow:
        flashColor = bright_yellow
        rectangle = yellow_button
    elif color == blue:
        flashColor = bright_blue
        rectangle = blue_button
    elif color == red:
        flashColor = bright_red
        rectangle = red_button
    elif color == green:
        flashColor = bright_green
        rectangle = green_button
    origSurf = display_screen.copy()  # PRESERVE ORIGINAL SURFACE
    flashSurf = pygame.Surface((buttonsize, buttonsize))  # TRANSPARENT OVERLAY FOR ANIMATION
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor

    for start, end, step in ((0, 255, 1), (255, 0, -1)):  # animation loop
        for alpha in range(start, end, animationSpeed * step):
            # FADE IN:Alpha 0→255 
            # Fade Out: Alpha 255→0
            checkForQuit()
            display_screen.blit(origSurf, (0, 0))  # reset to original
            flashSurf.fill((r, g, b, alpha))  # set transparency
            display_screen.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            fps_clock.tick(fps)  # MAINTAINING FPS TO 30
    display_screen.blit(origSurf, (0, 0))

# FUNCTION TO CREATE BUTTONS
def drawButtons():
    pygame.draw.rect(display_screen, yellow, yellow_button)
    pygame.draw.rect(display_screen, blue, blue_button)
    pygame.draw.rect(display_screen, red, red_button)
    pygame.draw.rect(display_screen, green, green_button)

# The background color change animation happens whenever the player finishes entering the entire pattern correctly
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor 
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((width_window, height_window))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):  # animation loop
        checkForQuit()
        display_screen.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        display_screen.blit(newBgSurf, (0, 0))

        drawButtons()  # redraw the buttons on top of the tint

        pygame.display.update()
        fps_clock.tick(fps)
    bgColor = newBgColor

def gameOverAnimation(color=white, animationSpeed=50):
    # flash the background
    origSurf = display_screen.copy()
    flashSurf = pygame.Surface(display_screen.get_size())
    flashSurf = flashSurf.convert_alpha()
    r, g, b = color
    for i in range(3):  # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step):  # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                display_screen.blit(origSurf, (0, 0))
                display_screen.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                fps_clock.tick(fps)

# TO GET WHERE MOUSE CLICKS
def getButtonClicked(x, y):
    if yellow_button.collidepoint((x, y)):
        return yellow
    elif blue_button.collidepoint((x, y)):
        return blue
    elif red_button.collidepoint((x, y)):
        return red
    elif green_button.collidepoint((x, y)):
        return green
    return None

if __name__ == '__main__':
    main()
