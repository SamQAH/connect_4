import sys, pygame
from pygame import Color, Surface
from pygame.locals import *
import random
import os
import math
import time
import copy

#initiate pygame and fonts
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


size = 600, 400
GREEN = (0, 255, 0)
DARKGREEN = (0,100,0)
RED = (255, 0, 0)
LIGHTRED = (255, 100, 100)
ORANGE = (255, 125, 0)
DARKRED = (150, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTGRAY = (200, 200, 200)
EMPTY = Color(0,0,0,0)

screen = pygame.display.set_mode(size)


#returns button surface, and rect
def button(text, font, fontsize, textcolour, backgroundcolour):
    Font = pygame.font.SysFont(font, fontsize)
    Text = Font.render(text, True, textcolour)
    button = pygame.Surface((Text.get_width()*1.2, Text.get_height()*1.2), pygame.SRCALPHA)
    pygame.draw.rect(button, backgroundcolour, (0,0,button.get_width(),button.get_height()),0,40)
    button.blit(Text, (Text.get_width()*0.1, Text.get_height()*0.1))
    
    return button
    

#reset button
reset = button("reset", "times", 30, LIGHTGRAY, RED)
resetPos = (10,100)
resetRect = reset.get_rect().inflate(10,10).move(resetPos)


#title
font = pygame.font.SysFont("calibre",100)
titleText = font.render('Connect 4', True, GREEN)
title = pygame.Surface((titleText.get_width()+40,titleText.get_height()+30), pygame.SRCALPHA)
title.blit(titleText, (20,15))
titlePos = (screen.get_width()/2-title.get_width()/2,20)

#start button
font = pygame.font.SysFont("bree serif",50)
startText = font.render('START',True, WHITE)
start = pygame.Surface((startText.get_width()+40,startText.get_height()+30), pygame.SRCALPHA)
pygame.draw.rect(start, DARKGREEN, (0,0,start.get_width(),start.get_height()),0,40)
start.blit(startText, (20,15))

startScreenPos = (screen.get_width()/2-start.get_width()/2,screen.get_height()/2-start.get_height()/2)

#start button border
startBorderRect = start.get_rect().inflate(10,10).move(startScreenPos)

#toggle bot button
font = pygame.font.SysFont("bree serif",50)
toggleText = font.render('1 player',True, WHITE)
toggleBot = pygame.Surface((toggleText.get_width()+40,toggleText.get_height()+30), pygame.SRCALPHA)
pygame.draw.rect(toggleBot, DARKRED, (0,0,toggleBot.get_width(),toggleBot.get_height()), 0,40)
toggleBot.blit(toggleText, (20,15))

toggleBotPos = (screen.get_width()/2-toggleBot.get_width()/2,screen.get_height()/2-toggleBot.get_height()/2+100)

#toggle bot border
toggleBotRect = toggleBot.get_rect().inflate(10,10).move(toggleBotPos)

#check mark
checkmark = pygame.Surface((50,50), pygame.SRCALPHA)
pygame.draw.polygon(checkmark, GREEN, ((25,0),(0,43.3),(50,43.3)))
pygame.draw.polygon(checkmark, GREEN, ((25,50),(0,6.7),(50,6.7)))

checkmarkPos = (screen.get_width()/2-toggleBot.get_width()/2+200,screen.get_height()/2-toggleBot.get_height()/2+100)

#7 by 6 board, chip size 50 by 50 circle radius 20
board = pygame.Surface((350, 300), pygame.SRCALPHA)
board.fill(GRAY)
for i in range(7):
    for j in range(6):
        pygame.draw.circle(board, WHITE, (25+i*50, 25+j*50), 20)
        
emptyBoard = board.copy()
boardPos = (screen.get_width()/2-board.get_width()/2,screen.get_height()/2-board.get_height()/2+20)

#turn text
font = pygame.font.SysFont("times",40)
turnText = font.render('Turn:',True, BLACK)
turnRed = pygame.Surface((turnText.get_width()+80,turnText.get_height()+20), pygame.SRCALPHA)
turnRed.blit(turnText, (10,10))
pygame.draw.circle(turnRed, RED, (turnText.get_width()+20, turnRed.get_height()/2), 10)
turnGreen = pygame.Surface((turnText.get_width()+80,turnText.get_height()+20), pygame.SRCALPHA)
turnGreen.blit(turnText, (10,10))
pygame.draw.circle(turnGreen, GREEN, (turnText.get_width()+20, turnGreen.get_height()/2), 10)

turnPos = (screen.get_width()/2-turnRed.get_width()/2,5)

#selcet player color
switchColorButtonGreen = button("switch color", "calibre", 40, BLACK, GREEN)
switchColorButtonRed = button("switch color", "calibre", 40, BLACK, RED)
switchColorPos = (screen.get_width()/2-switchColorButtonRed.get_width()/2, 350)
switchColorRect = switchColorButtonRed.get_rect().inflate(10,10).move(switchColorPos)

#exit button
exitButton = button("EXIT", "Times", 20, WHITE, DARKGREEN)
exitButtonPos = (screen.get_width()-exitButton.get_width()-20, 20)
exitButtonRect = exitButton.get_rect().inflate(5,5).move(exitButtonPos)






running = True
counter = 0
clickBuffer = 0
turn = 'red'
stage = "title"
enableBot = False
playerColor = "red"

victor = None
gameboard = []
emptygameboard = []
for i in range(7):
    gameboard.append([])
    emptygameboard.append([])

cursorhover = None








#graphic representaion of gameboard array
def update(B, S):
    for i, col in enumerate(B):
        for j, row in enumerate(col):
            if row == 'red':
                colour = RED
            elif row == 'green':
                colour = GREEN
            else:
                continue
            pygame.draw.circle(S, colour, (25+i*50, 275-j*50), 20)
    return S

#checks the victor
def checkvictor(B):
    def checkfor(P):
        pchip = []
        for i, col in enumerate(B):
            for j, row in enumerate(col):
                if row == P:
                    pchip.append((i, j))
                    
        for (x, y) in pchip:
            #check up, right, up right, down right
            if (x, y+1) in pchip and (x, y+2) in pchip and (x, y+3) in pchip:
                return True
            elif (x+1, y+1) in pchip and (x+2, y+2) in pchip and (x+3, y+3) in pchip:
                return True
            elif (x+1, y) in pchip and (x+2, y) in pchip and (x+3, y) in pchip:
                return True
            elif (x+1, y-1) in pchip and (x+2, y-2) in pchip and (x+3, y-3) in pchip:
                return True
        return False
        
    
    if checkfor("red"):
        return "red"
    if checkfor("green"):
        return "green"
    
    
    #checks if the entire board is filled
    fullcount = 0
    for col in B:
        fullcount += len(col)//6
    if fullcount == 7:
        return 'draw'
        
    return None


class Position:
    def __init__(self, B, P):
        self.currentPlayer = P
        self.oppPlayer = "green" if P == "red" else "red"
        self.board = B
        
    def victor(self):
        
        pchip = self.enu(self.oppPlayer)
                    
        for (x, y) in pchip:
            #check up, right, up right, down right
            if (x, y+1) in pchip and (x, y+2) in pchip and (x, y+3) in pchip:
                return -1
            elif (x+1, y+1) in pchip and (x+2, y+2) in pchip and (x+3, y+3) in pchip:
                return -1
            elif (x+1, y) in pchip and (x+2, y) in pchip and (x+3, y) in pchip:
                return -1
            elif (x+1, y-1) in pchip and (x+2, y-2) in pchip and (x+3, y-3) in pchip:
                return -1
            
        
        
        
        
        
        #checks if the entire board is filled
        fullcount = 0
        for col in self.board:
            fullcount += len(col)//6
        if fullcount == 7:
            return 'draw'
            
        return None
        
        
    def threats(self, forP):
        GB = self.enu(forP)
        threatPos = []
        for (x, y) in GB:
            scanArr = [[(x,y+1),(x,y+2),(x,y+3)],[(x+1,y+1),(x+2,y+2),(x+3,y+3)],[(x+1,y),(x+2,y),(x+3,y)],[(x+1,y-1),(x+2,y-2),(x+3,y-3)]]
            posT = []
            
            for t in scanArr:
                skip = False
                for i, (x, y) in enumerate(t):
                    if x < 0 or x > 7 or y < 0 or y > 6:
                        skip = True
                        break
                if skip == False:
                    posT.append(t)
                    
            
            for i, threats in enumerate(posT):
                for pos in threats:
                    if pos in GB:
                        posT[i].remove((pos))
                if len(threats) == 1:
                    #threatPos += 1#and the threat is not blocked
                    threatPos.append(threats[0])
                
        temp = []
        for cord in threatPos:
            if not(cord in temp):
                temp.append(cord)
        return temp
        
    def enu(self, forP):
        pchip = []
        for i, col in enumerate(self.board):
            for j, row in enumerate(col):
                if row == forP:
                    pchip.append((i, j))
        return pchip
        
    def legalMoves(self):
        legalMoves = [0,1,2,3,4,5,6]
        for i, col in enumerate(self.board):
            if len(col) == 6:
                legalMoves.remove(i)
        return legalMoves
        
    def evaluate(self):
        '''if self.victor != None:
            return -1'''
        playerChips = self.enu(self.currentPlayer)
        oppChips = self.enu(self.oppPlayer)
        currentPlayerBoardThreats = self.threats(self.currentPlayer)
        oppPlayerBoardThreats = self.threats(self.oppPlayer)
        
        C = 0
        O = 0
        for cord in currentPlayerBoardThreats:
            if not (cord in oppChips):
                if len(self.board[cord[0]]) == cord[1]:
                    C += 1
                elif cord[1]%2 == (0 if self.currentPlayer == "red" else 1):
                    C += 10
                else:
                    C += 1
                
                
        for cord in oppPlayerBoardThreats:
            if not (cord in playerChips):
                if len(self.board[cord[0]]) == cord[1]:
                    O += 1
                elif cord[1]%2 == (0 if self.currentPlayer == "red" else 1):
                    O += 10
                else:
                    O += 1
        
        return C/(C+O+1)
        
    def nextPositions(self):
        legalmoves = self.legalMoves()
        temp = [copy.deepcopy(self.board) for i in range(len(legalmoves))]
        possiblePositions = []
        cord = []
        for i, move in enumerate(legalmoves):
            temp[i][move].append(self.currentPlayer)
            possiblePositions.append(Position(temp[i], self.oppPlayer))
            cord.append((move,len(self.board[move])))
        return possiblePositions
        
    '''def likelyNextPositions(self):
        #priority
        #block oppenent's threats if applicable/accessible
        #increase current threats
        for Pos in self.nextPositions():
            
        oppPlayableThreats = []'''
        
        
        

def NSFW(B, P):#winning for the current player return 1, opponent return -1

    depth = 7 #bruteforcedepth + smartdepth
    
    startingPos = Position(B, P)
    
    def recursion(depth, B):
        bruteforcedepth = 3
        smartdepth = 4
        
        if B.victor() != None:
            return -1
        
        if depth == 0:
            B.evaluate()
            
        if depth <= smartdepth:
            
            evals = []
            
            for Pos in B.nextPositions():
                evals.append(Pos.evaluate())
                if -1 in evals:
                    return 1
                
                
            avg = 0
            for j in range(2):
                i = evals.pop(evals.index(max(evals)))
                avg += recursion(depth-1, B.nextPositions().pop(i))
            
            return avg/2
        else:
            evals = []
            L = 0
            
            for Pos in B.nextPositions():
                evals.append(recursion(depth-1, Pos))
                L += 1
                if -1 in evals:
                    return 1
            avg = 0
            for E in evals:
                avg += E
                
            return avg/L
            
    evals = []
    for i, Pos in enumerate(startingPos.nextPositions()):
        evals.append(recursion(depth, Pos))
        if -1 in evals:
            return startingPos.legalMoves[i]
    print(evals)
    return startingPos.legalMoves()[evals.index(min(evals))]
                
            
        
        
        
            
        


#connect 4 bot, takes a board position and the current colour's turn
def connectfish(B, P):
    #check for the first 5 moves
    
    
    #depth = 5
    
    def enuBoard(GB, P):
        pchip = []
        for i, col in enumerate(GB):
            for j, row in enumerate(col):
                if row == P:
                    pchip.append((i, j))
        return pchip
                
    def threats(GB):
        threatPos = []
        for (x, y) in GB:
            scanArr = [[(x,y+1),(x,y+2),(x,y+3)],[(x+1,y+1),(x+2,y+2),(x+3,y+3)],[(x+1,y),(x+2,y),(x+3,y)],[(x+1,y-1),(x+2,y-2),(x+3,y-3)]]
            posT = []
            
            for t in scanArr:
                skip = False
                for i, (x, y) in enumerate(t):
                    if x < 0 or x > 7 or y < 0 or y > 6:
                        skip = True
                        break
                if skip == False:
                    posT.append(t)
                    
            
            for i, threats in enumerate(posT):
                for pos in threats:
                    if pos in GB:
                        posT[i].remove((pos))
            if len(threats) == 1:
                #threatPos += 1#and the threat is not blocked
                threatPos.append(threats[0])
                
        return threatPos
        
    def legalMoves(GB):
        legalMoves = [0,1,2,3,4,5,6]
        for i, col in enumerate(GB):
            if len(col) == 6:
                legalMoves.remove(i)
        return legalMoves
        
    
    def evaluate(GB, P, OP):
        playerChips = enuBoard(GB, P)
        oppChips = enuBoard(GB, OP)
        currentPlayerBoardThreats = threats(playerChips)
        oppPlayerBoardThreats = threats(oppChips)
        
        C = 0
        O = 0
        for cord in currentPlayerBoardThreats:
            if not (cord in oppChips):
                C += 1
                
        for cord in oppPlayerBoardThreats:
            if not (cord in playerChips):
                O += 1
        
        return C/(C+O+1)
        
    
    #layer is depth of recursion, GB is B from connectfish, P is P from connect fish
    #each recursion check return the best eval for each position after the color makes a move if applicable
    #when comparing, find your best move from oppenent's worst move
    #when evaluating a possible position 1 is gureented win for the color in play, -1 is for opponent
    #
    #
    def recursionCheck(layer, P):
        
        vic = P.victor()
        if vic != None:
            #print("found victory for "+P)
            return -1
        
        if layer == 0:
            #return evaluate(GB, P, oppColor)
            return P.evaluate()

        else:
            possiblePositions = P.nextPositions()
                
            
            evals = []
            for pos in possiblePositions:
                evals.append(recursionCheck(layer-1, pos))
                

            best = evals[0]
            for ev in evals:
                if ev < best:
                    best = ev
                if best == -1:
                    return 1
            
            if not (1 in evals):
                avg = 0
                for e in evals:
                    avg += e
                avg /= len(evals)
                return avg
            
            
            return -best
            
            
    def startChecking(GB, P):
        depth = 5
        
        #preliminary check for obvious mates
        startPos = Position(GB, P)
        
        oppColor = "red" if P == "green" else "green"
        
        possiblePositions = startPos.nextPositions()
            
        evals = []
        for pos in possiblePositions:
            evals.append(recursionCheck(depth, pos))
            if -1 in evals:
                break
            
        best = evals[0]
        for ev in evals:
            if ev < best:
                best = ev
                
        print(evals)
        count = evals.count(best)
        if count > 1:
            R = random.randint(0, count-1)
            for i in range(R):
                evals[evals.index(best)] = None
                
        return startPos.legalMoves()[evals.index(best)]
        
    
    return startChecking(B, P)


                
        




# main program
while running:
    clock.tick(60)
    
    screen.fill(WHITE)
    
    
    if clickBuffer > 0:
        clickBuffer -= 1
        
    
    for event in pygame.event.get():
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            f.close()
    
    
    
    if stage == "title":
        screen.blit(start,startScreenPos)
        screen.blit(title,titlePos)
        screen.blit(toggleBot,toggleBotPos)
        screen.blit(exitButton, exitButtonPos)
        
        if enableBot:
            screen.blit(checkmark,checkmarkPos)
            if playerColor == "red":
                screen.blit(switchColorButtonRed, switchColorPos)
            else:
                screen.blit(switchColorButtonGreen, switchColorPos)
        
        # detects mouse motion or button down
        #if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            # mouse and start button collision detection
        if startBorderRect.collidepoint(mouse_pos):
            
            # draws the border of the start button if mouse is colliding with the start button
            pygame.draw.rect(screen, GREEN, startBorderRect, 20,40)
            if mouse_press[0] and clickBuffer == 0:
                stage = "game"
                clickBuffer = 30
                f = open("stored_positions.txt", "w")
        
        #ai button
        if toggleBotRect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GREEN, toggleBotRect, 20, 40)
            if mouse_press[0] and clickBuffer == 0:
                enableBot = not enableBot
                clickBuffer = 30
                
                
        elif switchColorRect.collidepoint(mouse_pos) and enableBot == True:
            pygame.draw.rect(screen, DARKGREEN, switchColorRect, 5, 40)
            if mouse_press[0] and clickBuffer == 0:
                playerColor = "red" if playerColor == "green" else "green"
                clickBuffer = 30
                print(playerColor)

        elif exitButtonRect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLACK, exitButtonRect, 5, 10)
            if mouse_press[0] and clickBuffer == 0:
                pygame.quit()
            
            
                    
    elif stage == 'game':#checkvictor before bot's move
        if turn == 'red':
            screen.blit(turnRed, turnPos)
        elif turn == 'green':
            screen.blit(turnGreen, turnPos)
            
        screen.blit(board, boardPos)
        screen.blit(reset, resetPos)
        screen.blit(exitButton, exitButtonPos)
        
        if resetRect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DARKRED, resetRect, 5, 40)
            if mouse_press[0] and clickBuffer == 0:
                board = emptyBoard.copy()
                gameboard = copy.deepcopy(emptygameboard)
                victor = None
                clickBuffer = 30
                turn = "red"
                
                
        elif exitButtonRect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLACK, exitButtonRect, 5, 10)
            if mouse_press[0] and clickBuffer == 0:
                board = emptyBoard.copy()
                gameboard = copy.deepcopy(emptygameboard)
                victor = None
                clickBuffer = 30
                turn = "red"
                f.close()
                stage = "title"
                screen.fill(WHITE)
                continue

        if victor != None:
            if victor == 'red':
                colour = RED
            elif victor == 'green':
                colour = GREEN
            elif victor == 'draw':
                colour = GRAY
            victorText = font.render(victor, True, colour)
            screen.blit(victorText, (500, 100))
        
        
        
        mousehover = None
        for i in range(7):
            if 125+i*50 < mouse_pos[0] < 175+i*50:
                mousehover = i
                break
        
        
        if enableBot == True and turn != playerColor and victor == None and clickBuffer == 0:
            move = connectfish(gameboard, turn)
            gameboard[move].append(turn)
            board = update(gameboard, board)
            victor = checkvictor(gameboard)
            f.write(str(gameboard))
            f.write("\n")
            
            clickBuffer = 30
            
            if turn == 'red':
                turn = 'green'
            elif turn == 'green':
                turn = 'red'
        
        
        
        if mousehover != None and victor == None:
            '''
            if turn == 'red':
                screen.blit(redchipOutline, )
            elif turn == 'green':
                screen.blit(greenchipOutline, )
                '''
                
                
            if mouse_press[0] and clickBuffer == 0 and len(gameboard[mousehover]) != 6:
                print("played")
                gameboard[mousehover].append(turn)
                board = update(gameboard, board)
                victor = checkvictor(gameboard)
                f.write(str(gameboard))
                f.write("\n")

                clickBuffer = 30
                
                if turn == 'red':
                    turn = 'green'
                elif turn == 'green':
                    turn = 'red'
        
        
        
        
        
        
        
        
        
    pygame.display.update()
