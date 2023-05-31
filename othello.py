# digital rendition of the board game othello

import turtle
import random

# makeBoard creates a visual representation of the gameboard with turtle graphics
def makeBoard():
    turtle.ht()
    turtle.setworldcoordinates(0,0,9,9)
    turtle.penup()
    screen = turtle.getscreen()
    screen.tracer(0)
    count = 0
    while count < 8: #row labels
        turtle.goto(.5,8 - count)
        turtle.write(count)
        count += 1
    count = 0
    while count < 8: #column labels
        turtle.goto(count + 1,8.5)
        turtle.write(count)
        count += 1
    turtle.shape('square')
    turtle.color('green')
    turtle.turtlesize(stretch_wid=2.5)
    count1 = 1
    while count1 < 9: #create board squares
        count2 = 1
        while count2 < 9:
            turtle.goto(count1, count2)
            turtle.stamp()
            count2 += 1
        count1 += 1
    screen.update()
    return

# firstTokens uses turtle graphics to create the visual representation of the first
# four tokens present at the start of the game
def firstTokens():
    turtle.goto(4,5)
    turtle.dot(50,'white')
    turtle.goto(5,4)
    turtle.dot(50,'white')
    turtle.goto(5,5)
    turtle.dot(50,'black')
    turtle.goto(4,4)
    turtle.dot(50,'black')
    return

# makeBoardMatrix creates a two dimentional list representation of the gameboard
def makeBoardMatrix():
    board = []
    count = 0
    while count < 8: #rows
        count2 = 0
        column = []
        while count2 < 8: #columns
            column += [0] #0 to indicate empty
            count2 += 1
        board += [column]
        count += 1
    board[4][3] = 'black' #inital four tokens
    board[3][4] = 'black'
    board[4][4] = 'white'
    board[3][3] = 'white'
    return board

# isValidMove evalutates spaces surrounding the place of proposed token placement (PPTP)
# and their related candidate lines to determine legality of the move
# inputs: 1) matrix representation of the current board, 2) integer indicating row of the PPTP
# 3) integer indicating colum of the PPTP, 4) string indicating the color of the token to be placed
# output: boolean value indicating if the move is legal (True) or illegal (False)
def isValidMove(board,row,col,color):
    if board[row][col] != 0: #prohibt placing token on occupied space
        return False
    r = 0
    for rows in board:
        c = 0
        for cols in rows:
            if r != row or c != col:
                if abs(r-row) <= 1 and abs(c-col) <= 1: #limits scope to only adjacent spaces
                    if board[r][c] != color and board[r][c] != 0: #true iff occupied by opponent token
                        searching = True
                        delta_y = c - col #movement up/down from previous token in line
                        delta_x = r - row #movement left/right form previous token in line
                        y = delta_y + c #col of next token
                        x = delta_x + r #row of next token
                        while searching:
                            if y > 7 or x > 7: #off the board
                                searching = False
                            elif board[x][y] == 0: #empty space
                                searching = False
                            elif board[x][y] == color: #occupied by friendly token
                                return True
                            else: #occupied by opponent token
                                y += delta_y #col of next token
                                x += delta_x #row of next token
            c += 1
        r += 1
    return False

# getValidMoves examines every space on the board and calls the function isValidMove
# to determine the validity/legality of each
# inputs: 1) matrix representation of the current board, 2) string indicating the color
# of the tokens belonging to the player currently taking their turn
# output: a list of tuples containg pairs of integers representing the coordinates of
# all the valid/legal moves that the player could make
def getValidMoves(board,color):
    moves = [] #list of valid moves
    r = 0
    for rows in board:
        c = 0
        for cols in rows:
            if isValidMove(board,r,c,color): #true if move is valid
                moves += [(r,c)]
            c += 1
        r += 1
    return moves

# selectNextPlay randomly chooses a move for the computer to make out of all the valid
# moves currently availble
# input: matrix representation of the current board
# output: tuple containing a pair of integers representing the coordinates of the computer's next move
def selectNextPlay(board):
    moves = getValidMoves(board,'white')
    selection = random.randint(0,len(moves) - 1)
    return moves[selection]

# convertCoordinates converts the board's row and column coordinates to turtle's x and y coordinates
# inputs: 1) integer representing the row of a position on the board, 2) integer
# representing the column of a position on the board
# outputs: 1) integer representing the x coordinate of a position in the turtle graphics
# depcition of the board, 2) integer representing the y coordinate of a position in the
# turtle graphics depiction of the board
def convertCoordinates(row,col):
    x = row + 1
    y = 8  - col
    return x, y

# tokenFlip identifies tokens to be flipped, simulates the flipping with turtle
# graphics, and then updates the values in the matrix representation of the board
# inputs: 1) matrix representation of the current board, 2) integer indicating row where
# the initial token was placed 3) integer indicating column where the initial token was placed,
# 4) string indicating the color of the token placed
# output: updated matrix representation of the current board
# note: tokenFlip only ever called after move has been confirmed to be valid
def tokenFlip(board,row,col,color):
    fliplist = [(row,col)] #list of tokens to be flipped
    r = 0
    for rows in board:
        c = 0
        for cols in rows:
            if r != row or c != col:
                if abs(r-row) <= 1 and abs(c-col) <= 1: #limits scope to only adjacent spaces
                    if board[r][c] != color and board[r][c] != 0: #true iff occupied by opponent token
                        searching = True
                        maybeflip = [(r,c)] #list of tokens to be flipped if friendlly token at end of line
                        delta_y = c - col #movement up/down from previous token in line
                        delta_x = r - row #movement left/right form previous token in line
                        y = delta_y + c #col of next token
                        x = delta_x + r #row of next token
                        while searching:
                            if y > 7 or x > 7: #off the board
                                searching = False
                            elif board[x][y] == 0: #empty space
                                searching = False
                            elif board[x][y] == color: #occupied by friendly token
                                searching = False
                                fliplist += maybeflip #friendly token identified, all intervening tokens confirmed for flipping
                            else: #occupied by opponent token
                                maybeflip += [(x,y)]
                                y += delta_y #col of next token
                                x += delta_x #row of next token
            c += 1
        r += 1
    for coordinates in fliplist:
        turtle.goto(convertCoordinates(coordinates[0],coordinates[1]))
        turtle.dot(50,color) #token flip simulation
        board[coordinates[0]][coordinates[1]] = color #update matrix
    return board

# gameOver counts the final number of tokens each player had on the board and determines
# which side won based on who had the greater sum, it then outputs this info to the screen
# input: matrix representation of the final board formation
def gameOver(board):
    turtle.color('black')
    results = {} #dictionary to hold final results for black and white respectively
    results['white'] = 0
    results['black'] = 0
    for row in board:
        for col in row:
            if col == 'white': #space occupied by white token, point for white
                results['white'] += 1
            elif col == 'black': #space occupied by black token, point for black
                results['black'] += 1
    turtle.clear()
    turtle.goto(4.5,4)
    if results['white'] < results['black']: #human player (black) is the winner
        turtle.write('Congrats! Black is the winner!', align='center', font=('Arial',20,'normal'))
    elif results['white'] > results['black']: #computer (white) is the winner
        turtle.write('Best of luck next time. White is the winner.', align='center', font=('Arial',20,'normal'))
    else: #no winner, scores are equal, result is a tie
        turtle.write("It's a tie!", align='center', font=('Arial',20,'normal'))
    turtle.goto(4.5,3)
    turtle.write('Final Score: White ' + str(results['white']) + ' and Black ' + str(results['black']), align='center', font=('Arial',10,'normal'))

def main():
    turtle.ht()
    makeBoard()
    firstTokens()
    board = makeBoardMatrix()
    playerinput = turtle.textinput('','Enter row,col: ')
    while playerinput != '':
        if getValidMoves(board,'black') != []: #player turn, check if moves available
            while len(str(playerinput)) != 3 or ',' not in str(playerinput): #help protect against problems caused by most incorrect input and the indexing used to identify row and col
                playerinput = turtle.textinput('',"Sorry, that's not a valid move. Please enter row,col: ")
            playerinput = eval(playerinput)
            row = playerinput[1] #based on graphics display, input is initially backwards
            col = playerinput[0]
            while not isValidMove(board,row,col,'black'):
                playerinput = turtle.textinput('',"Sorry, that's not a valid move. Please enter row,col: ")
                playerinput = eval(playerinput)
                row = playerinput[1]
                col = playerinput[0]
            board = tokenFlip(board, row, col, 'black')
        if getValidMoves(board,'white') != []: #computer turn, begin with check to see if moves avaiable
            comp_input = selectNextPlay(board)
            board = tokenFlip(board, comp_input[0],comp_input[1], 'white')
        if getValidMoves(board,'black') != []: #player turn again, check if moves available
            playerinput = turtle.textinput('','Enter row,col: ')
        else:
            if getValidMoves(board,'white') == []: #if true, no moves avaiable for white or black, includes full board senario
                playerinput = '' #end loop, gameover
    gameOver(board)

if __name__ == '__main__':
    main()
