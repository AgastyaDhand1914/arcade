#AUTHOR : AGASTYA DHAND
import sys, random, pygame
from pygame.locals import *


#colors

neon_red = (255, 69, 0)       
neon_green = (57, 255, 20) 
neon_blue = (0, 17, 255)     
neon_yellow = (255, 255, 0)    
neon_purple = (218, 112, 214) 
neon_cyan = (0, 255, 255)     

arcade_black = (10, 10, 10) 
arcade_gray = (33, 33, 33)  
arcade_light_gray = (77, 77, 77)

highlight_glow = (255, 140, 0) 
highlight_border = (255, 20, 147) 

object_color_tuple = (neon_red, neon_green, neon_blue, neon_yellow, neon_purple, neon_cyan)

background = arcade_black
light_background = arcade_gray
box_background = arcade_light_gray
highlight_color = highlight_glow

#shapes

Donut = 'donut' 
Square = 'square' 
Diamond = 'diamond' 
Cross = 'cross' 
Oval = 'oval' 

object_shape_tuple = (Donut, Square, Diamond, Cross, Oval)

#total objects = 6 x 5 x 2 = 60
#therefore board dimensions will be same - 6x10

#constants

FPS = 30
window_width = 640
window_height = 480
box_size = 40
gap_size = 10
reveal_speed = 8

board_columns = 10
board_rows = 6

margin_x = int((window_width - (board_columns * (box_size + gap_size))) / 2)
margin_y = int((window_height - (board_rows * (box_size + gap_size))) / 2)


#creating a 2-D array to keep track of boxes revealed
def makeRevealBoxData(truth_value):
    result = []
    for i in range(board_columns):  
        result.append([truth_value] * board_rows)
    return result


#generating mainBoard with objects at random places
def randomBoard():
    objects =[]
    for color in object_color_tuple:
        for shape in object_shape_tuple:
            objects.append((shape, color))
    
    random.shuffle(objects)
    required_num_of_objects = int(board_rows * board_columns) / 2
    objects = objects[:int(required_num_of_objects)] * 2
    random.shuffle(objects)

    board = []
    for x in range(board_columns):
        col = []
        for y in range(board_rows):
            col.append(objects[0])
            del objects[0]
        board.append(col)
    
    return board

#getting top left coordinates of a box
def boxCoords(Box_x, Box_y):
    top = Box_y * (box_size + gap_size) + margin_y
    left = Box_x * (box_size + gap_size) + margin_x
    return (left, top)

#getting box coordinates (pair of indices (0-9, 0-5)) in form of pair of indices
def getBoxIndex(x, y):
    for i in range(board_columns):
        for j in range(board_rows):
            left, top = boxCoords(i, j)
            boxRect = pygame.Rect(left, top, box_size, box_size)
            #checking if (x, y) is in region enclosed by boxRect
            if boxRect.collidepoint(x, y):
                return (i, j)
    return (None, None)

#getting information about an object
def getObjectInfo(mainBoard, Box_x, Box_y):
    return mainBoard[Box_x][Box_y][0], mainBoard[Box_x][Box_y][1]

#drawing an object in the box
def drawObject(shape, color, x, y):
    HALF = int(box_size * 0.5)
    QUARTER = int(box_size * 0.25)

    left, top = boxCoords(x, y)

    if shape == Donut:
        pygame.draw.circle(DISPLAYSURF, color, (left + HALF, top + HALF), HALF - 5)
        pygame.draw.circle(DISPLAYSURF, background, (left + HALF, top + HALF), QUARTER - 5)
    elif shape == Square:
        pygame.draw.rect(DISPLAYSURF, color, (left + int(QUARTER // 2), top + int(QUARTER // 2), box_size - QUARTER, box_size - QUARTER))
    elif shape == Diamond:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + HALF, top), (left + box_size - 1, top + HALF), (left + HALF, top + box_size - 1), (left, top + HALF)))
    elif shape == Cross:
        offset = int(QUARTER / 2)
        reduced_size = int(box_size - QUARTER)
        pygame.draw.line(DISPLAYSURF, color, (left + offset, top + offset), (left + offset + reduced_size, top + offset + reduced_size), 3)
        pygame.draw.line(DISPLAYSURF, color, (left + offset, top + offset + reduced_size), (left + offset + reduced_size, top + offset), 3)
    elif shape == Oval:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + QUARTER, box_size, HALF))


#main function
def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #main display surafce
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('MEMORY MATCH PUZZLE')

    #coordinates of mouse event
    current_x = 0
    current_y = 0

    #initial state of board and object boxes
    mainBoard = randomBoard()
    revealedBoxObject = makeRevealBoxData(False)

    #first box clicked 
    #at start or after selecting unmatched pair, this is reset to be implemented for another pair
    first_box_selection = None

    DISPLAYSURF.fill(background)
    startGameAnimation(mainBoard)

    #main game loop
    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(background)
        drawCurrentBoard(mainBoard, revealedBoxObject)

        #event handling loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                #cleaning up and shutting down modules and componenets (display surface) set up
                #by pygame.init()
                pygame.quit()
                #terminate program
                sys.exit()
            #mouse cursor moves
            elif event.type == MOUSEMOTION:
                current_x, current_y = event.pos
            #mouse cursor click
            elif event.type == MOUSEBUTTONUP:
                current_x, current_y = event.pos
                mouse_clicked = True
        
        #fetching index pair (0-9, 0-5) of clicked box
        index_pair = getBoxIndex(current_x, current_y)
        Box_x, Box_y = index_pair

        if Box_x is not None and Box_y is not None:
            #mouse cursor over a box
            if not revealedBoxObject[Box_x][Box_y]:
                #if object box is covered (plain white box), show highlight effect
                highlightBox(Box_x, Box_y)
                if mouse_clicked:
                    #show object in box if mouse clicked on it
                    boxRevealAnimation(mainBoard, [(Box_x, Box_y)])
                    revealedBoxObject[Box_x][Box_y] = True

                    if first_box_selection is None:
                        #first box clicked
                        first_box_selection = (Box_x, Box_y)
                    else:
                        #second box clicked - check for match
                        reference_shape, reference_color = getObjectInfo(mainBoard, first_box_selection[0], first_box_selection[1])
                        current_shape, current_color = getObjectInfo(mainBoard, Box_x, Box_y)

                        if reference_shape != current_shape or reference_color != current_color:
                            #not a match, so hide both objects
                            pygame.time.wait(1000)
                            boxCoverAnimation(mainBoard, [(first_box_selection[0], first_box_selection[1]), (Box_x, Box_y)])
                            revealedBoxObject[first_box_selection[0]][first_box_selection[1]] = False
                            revealedBoxObject[Box_x][Box_y] = False
                        elif wonTheGame(revealedBoxObject):
                            #game win effect
                            gameWonEffect(mainBoard)
                            pygame.time.wait(3000)

                            #reset game to intial state
                            mainBoard = randomBoard()
                            revealedBoxObject = makeRevealBoxData(False)

                            drawCurrentBoard(mainBoard, revealedBoxObject)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            startGameAnimation(mainBoard)
                        
                        #reset first_box_selection regardless of match or not
                        first_box_selection = None

        #update display surface on continuously
        pygame.display.update()
        #ensuring constant FPS rendering
        FPSCLOCK.tick(FPS)

#making box cover
def drawBox(board, boxes, coverage):
    for box in boxes:
        left, top = boxCoords(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, background, (left, top, box_size, box_size))
        shape, color = getObjectInfo(board, box[0], box[1])
        drawObject(shape, color, box[0], box[1])

        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, box_background, (left, top, coverage, box_size))
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)

#box cover and reveal sequence
def boxRevealAnimation(board, boxes_to_reveal):
    for coverage in range(box_size, -reveal_speed - 1, -reveal_speed):
        drawBox(board, boxes_to_reveal, coverage)

def boxCoverAnimation(board, boxes_to_cover):
    for coverage in range(0, box_size + reveal_speed, reveal_speed):
        drawBox(board, boxes_to_cover, coverage)


#making entire board
def drawCurrentBoard(board, revealed):
    for box_x in range(board_columns):
        for box_y in range(board_rows):
            left, top = boxCoords(box_x, box_y)
            if not revealed[box_x][box_y]:
                #if object is covered, display a box
                pygame.draw.rect(DISPLAYSURF, box_background, (left, top, box_size, box_size))
            else:
                #object revealed, display it
                shape, color = getObjectInfo(board, box_x, box_y)
                drawObject(shape, color, box_x, box_y)

#highlighting effect
def highlightBox(Box_x, Box_y):
    left, top = boxCoords(Box_x, Box_y)
    #border effect when cursor hovers on box
    pygame.draw.rect(DISPLAYSURF, highlight_color, (left - 5, top - 5, box_size + 10, box_size + 10), 4)

#start game animation
def startGameAnimation(board):
    covered = makeRevealBoxData(False)
    boxes = []
    for x in range(board_columns):
        for y in range(board_rows):
            boxes.append((x, y))
    random.shuffle(boxes)
    
    #reveal and cover boxes in groups to give clues to user
    box_groups = []
    for i in range(0, len(boxes), 8):
        box_groups.append(boxes[i:i+8])
        #making groups of 8 objects at once 
    
    for group in box_groups:
        boxRevealAnimation(board, group)
        boxCoverAnimation(board, group)
        #revealing each group one at a time



#checking for win
def wonTheGame(revealedBoxes):
    #all elements in revealedBoxObject array (2D) must be True, meaning all objects are revealed
    for i in revealedBoxes:
        if False in i:
            return False
    return True


#after winning game
def gameWonEffect(board):
    covered = makeRevealBoxData(True)
    for i in range(10):
        #changing background color for a small effect, after some time game wouold be reset as in main()
        color = light_background if (i % 2 == 0) else background
        DISPLAYSURF.fill(color)
        drawCurrentBoard(board, covered)
        pygame.display.update()
        pygame.time.wait(300)


#main function called manually
if __name__ == '__main__':
    main()