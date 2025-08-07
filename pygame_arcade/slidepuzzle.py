#AUTHOR : AGASTYA DHAND
import sys, random, pygame
from pygame.locals import *


#colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)
gray = (100, 100, 100) 
dark_gray = (66, 64, 64)
light_gray = (189, 183, 183)

text_color = (255, 239, 64)
tile_color = (41, 16, 54)  
tile_text_color = (0, 255, 255) 
background = (207, 8, 84)
border_color = (26, 2, 3) 


#directions

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#constants

#4 x 4 board of 15 tiles, one empty space
board_size = 4
#square tile with side 80 pixels
tile_size = 80
#no. of moves for shuffling
difficulty = 50

#window dimensions
window_width = 640
window_height = 480

margin_x = int((window_width - (tile_size * board_size + (board_size - 1))) / 2)
margin_y = int((window_height - (tile_size * board_size + (board_size - 1))) / 2)

move_speed = 20
FPS = 30

#main function
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_RECT, RESET_SURF, NEW_RECT, NEW_SURF, SOLVE_RECT, SOLVE_SURF
    pygame.init()
    
    #base surface
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height))

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('SLIDER PUZZLE')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
   
    #reset, new game and solve buttons
    RESET_SURF, RESET_RECT = makeText('Reset', text_color, tile_color, window_width - 120, window_height - 90) 
    NEW_SURF, NEW_RECT = makeText('New Game', text_color, tile_color, window_width - 120, window_height - 60)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve', text_color, tile_color, window_width - 120, window_height - 30)

    #creating main board and corresponding solution board
    #difficulty[] represents the number of moves
    mainBoard, correct_sequence = createPuzzle(difficulty)
    solution = getSolutionBoard()
    moveset = []

    #main game loop
    while True:
        display_text = ''
        #if there exists any direction to slide tile in
        direction_to_slide = None

        #check for win
        if mainBoard == solution:
            display_text = 'Puzzle Solved, You Win!'
        
        drawBoard(mainBoard, display_text)

        #check if player quit
        checkQuit()
        #check mouse click
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                #get where mouse clicked
                clicked_x, clicked_y = getClickedTile(mainBoard, event.pos[0], event.pos[1])

                if (clicked_x, clicked_y) == (None, None):
                    #not clicked on board tiles, so check on all the other buttons
                    if RESET_RECT.collidepoint(event.pos):
                        #clicked reset, resetting board but not correct_sequence
                        resetAnimation(mainBoard, moveset)
                        moveset = []
                    elif NEW_RECT.collidepoint(event.pos):
                        #clickes on new game, generate new mainBoard, sequence
                        mainBoard, correct_sequence = createPuzzle(difficulty)
                        moveset = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, correct_sequence + moveset)
                        moveset = []
                else:
                    #check if tile clicked on is next to the empty space
                    space_x, space_y = getSpacePos(mainBoard)

                    #set direction_to_slide
                    if clicked_x == space_x + 1 and clicked_y == space_y:
                        direction_to_slide = LEFT
                    elif clicked_x == space_x - 1 and clicked_y == space_y:
                        direction_to_slide = RIGHT
                    elif clicked_x == space_x and clicked_y == space_y + 1: #clicked_y below space_y
                        direction_to_slide = UP
                    elif clicked_x == space_x and clicked_y == space_y - 1: #space_y below clicked_y
                        direction_to_slide = DOWN
            
            elif event.type == KEYUP:
                #pressed key instead of clicking
                #check if user press key to slide the tile
                if event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    direction_to_slide = RIGHT
                elif event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    direction_to_slide = LEFT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    direction_to_slide = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    direction_to_slide = DOWN
        
        if direction_to_slide:
            #slide operation commencement
            slideAnimation(mainBoard, direction_to_slide, 'Click on Tile or use Arrow or WASD keys to slide', 8)
            finishMove(mainBoard, direction_to_slide)
            #update moveset
            moveset.append(direction_to_slide)
        
        #update display
        pygame.display.update()
        #ensure const FPS in render
        FPSCLOCK.tick(FPS)

#check if quit
def checkQuit():
    #each event checked is 'consumed'
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        #non escape key KEYUP events are also consumed, they must be added back to the event queue
        #add other KEYUP event objects back
        pygame.event.post(event)

#get solution board
def getSolutionBoard():

    #2D array (board) with tiles in solved state
    # for 4x4, solution: [[1, 5, 9, 13],[2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, None]]
    num = 1
    board = []
    for i in range(board_size):
        col = []
        for y in range(board_size):
            col.append(num)
            num += board_size
        board.append(col)
        #difference (13 + 4 - 2) = (14 + 4 - 3) = (15 + 4 - 4) = 15
        #reset num to get next iteration's elements
        num -= board_size * board_size - 1
    
    #set empty space at last
    board[board_size - 1][board_size - 1] = None
    return board

#get position of empty space
def getSpacePos(board):
    for x in range(board_size):
        for y in range(board_size):
            if board[x][y] == None:
                return (x, y)

#check if slide operation is possible

def isValidMove(board, move):
    space_x, space_y = getSpacePos(board)
    #check if space is not in invalid positions for a given move
    up_possible = (move == UP and space_y != board_size - 1)
    down_possible = (move == DOWN and space_y != 0)
    left_possible = (move == LEFT and space_x != board_size - 1)
    right_possible = (move == RIGHT and space_x != 0)

    #since there re 4 different moves, at a time other 3 possibilities will always be False
    #if the remaining possibilty comes out to be True, we have a valid move
    return (True in (up_possible, down_possible, left_possible, right_possible))

#sliding operation on board
def finishMove(board, move):
    space_x, space_y = getSpacePos(board)

    if move == UP:
        board[space_x][space_y], board[space_x][space_y + 1] = board[space_x][space_y + 1], board[space_x][space_y]
        #space_y is above space_y + 1 index
    elif move == DOWN:
        board[space_x][space_y], board[space_x][space_y - 1] = board[space_x][space_y - 1], board[space_x][space_y]
    elif move == LEFT:
        board[space_x][space_y], board[space_x + 1][space_y] = board[space_x + 1][space_y], board[space_x][space_y]
    elif move == RIGHT:
        board[space_x][space_y], board[space_x - 1][space_y] = board[space_x - 1][space_y], board[space_x][space_y]


#to make the puzzle, random moves need to be performed on solution board
def makeRandomMove(board, lastMove = None):
    possible_moves = [UP, DOWN, LEFT, RIGHT]

    #remove from list those moves which are either:
    # -Not Valid (isValidMove fn returns false)
    # -opposite of 'lastMove' (UP - DOWN or LEFT - RIGHT)

    if lastMove == DOWN or not isValidMove(board, UP):
        possible_moves.remove(UP)
    if lastMove == UP or not isValidMove(board, DOWN):
        possible_moves.remove(DOWN)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        possible_moves.remove(LEFT)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        possible_moves.remove(RIGHT)
    
    #returning a random move to perform
    return random.choice(possible_moves)

#getting top left coordinates of tile in pixels
def getTileCoords(tile_x, tile_y):
    left = margin_x + (tile_size * tile_x) + tile_x - 1
    top = margin_y + (tile_size * tile_y) + tile_y - 1
    return (left, top)

#getting coords (0-3, 0-3) of tile clicked on
def getClickedTile(board, x, y):
    for tile_x in range(board_size):
        for tile_y in range(board_size):
            left, top = getTileCoords(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, tile_size, tile_size)
            if tile_rect.collidepoint(x, y):
                return tile_x, tile_y
    return None, None

#making tile on board
def drawTile(tile_x, tile_y, tile_number, adjx = 0, adjy = 0):
    #adjx and adjy determine position of tile w.r.t left, top of tile
    left, top = getTileCoords(tile_x, tile_y)
    pygame.draw.rect(DISPLAYSURF, tile_color, (left + adjx, top + adjy, tile_size, tile_size))
    TEXT_SURF = BASICFONT.render(str(tile_number), True, tile_text_color)
    TEXT_RECT = TEXT_SURF.get_rect()
    TEXT_RECT.center = left + int(tile_size / 2) + adjx, top + int(tile_size / 2) + adjy

    DISPLAYSURF.blit(TEXT_SURF, TEXT_RECT)

#making text
def makeText(text, color, bgcolor, top, left):
    #create surf and rect objects for text
    TEXT_SURF = BASICFONT.render(text, True, color, bgcolor)
    TEXT_RECT = TEXT_SURF.get_rect()
    TEXT_RECT.topleft = (top, left)

    return (TEXT_SURF, TEXT_RECT)

#drawing board
def drawBoard(board, text):
    DISPLAYSURF.fill(background)
    #adding main text
    if text: 
        TEXT_SURF, TEXT_RECT = makeText(text, text_color, background, 5, 5)
        DISPLAYSURF.blit(TEXT_SURF, TEXT_RECT) 

    #adding tiles
    for tile_x in range(board_size): 
        for tile_y in range(board_size): 
            if board[tile_x][tile_y]: 
                drawTile(tile_x, tile_y, board[tile_x][tile_y])
    
    #making border of board
    left, top = getTileCoords(0, 0)
    width = height = board_size * tile_size
    pygame.draw.rect(DISPLAYSURF, border_color, (left - 4, top - 4, width + 10, height + 10), 4)

    #adding buttons
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

#sliding 
def slideAnimation(board, direction_to_slide, message, speed):
    space_x, space_y = getSpacePos(board)
    #get coords of tile to move
    if direction_to_slide == UP:
        move_x = space_x
        move_y = space_y + 1
    elif direction_to_slide == DOWN:
        move_x = space_x
        move_y = space_y - 1
    elif direction_to_slide == LEFT:
        move_x = space_x + 1
        move_y = space_y
    elif direction_to_slide == RIGHT:
        move_x = space_x - 1
        move_y = space_y
    
    drawBoard(board, message)
    #creating copy of tile to move
    BASE_SURF = DISPLAYSURF.copy()
    #drawing empty space tile on tile to move
    tile_left, tile_top = getTileCoords(move_x, move_y)
    pygame.draw.rect(BASE_SURF, background, (tile_left, tile_top, tile_size, tile_size))

    for i in range(0, tile_size, speed):
        #sliding effect
        checkQuit()
        DISPLAYSURF.blit(BASE_SURF, (0, 0))

        #drawing tile closer and closer each frame to give sliding effect
        if direction_to_slide == UP:
            drawTile(move_x, move_y, board[move_x][move_y], 0, -i)
        elif direction_to_slide == DOWN:
            drawTile(move_x, move_y, board[move_x][move_y], 0, i)
        elif direction_to_slide == LEFT:
            drawTile(move_x, move_y, board[move_x][move_y], -i, 0)
        elif direction_to_slide == RIGHT:
            drawTile(move_x, move_y, board[move_x][move_y], i, 0)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# make the puzzle
def createPuzzle(number_of_moves):
    sequence = []
    #getting the solved state of board
    board = getSolutionBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)

    lastMove = None
    for i in range(number_of_moves):
        #generate random move and move tile and empty space
        random_move = makeRandomMove(board, lastMove)
        slideAnimation(board, random_move, 'Generating new Puzzle...', int(tile_size / 3))
        finishMove(board, random_move)
        sequence.append(random_move)
        lastMove = random_move
    
    return (board, sequence)

#board reset
def resetAnimation(board, moveset):
    #moveset contains all moves (directions to empty space) performed by user
    #so to get back the initial solved state of board, moveset is performed in reverse

    copy_moveset = moveset[::]
    reverse_moveset = copy_moveset[::-1]

    for move in reverse_moveset:
        if move == UP:
            opp_move = DOWN
        elif move == DOWN:
            opp_move = UP
        elif move == LEFT:
            opp_move = RIGHT
        elif move == RIGHT:
            opp_move = LEFT
        
        #performing reverse move
        slideAnimation(board, opp_move, '', int(tile_size / 2))
        finishMove(board, opp_move)

#calling main function
if __name__ == '__main__':
    main()