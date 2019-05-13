#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import copy
import random
import sys

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.utility = None
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently plays randomly.
    def aiPlay(self, depth, computer):
        # self.eval(computer)
        # Need to generate tree here
        # 1. Find all possible 7 moves and their children based on depth - Dome
        # 2. Apply utility moves on the leaf nodes - Done
        self.generateSuccessors(depth - 1, computer)
        # 3. Find the best move based on min-max algorithm - Done
        column = self.selectBestMove(computer)
        result = self.playPiece(column)
        if not result:
            self.aiPlay(depth, computer)
        else:
            print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, column+1))
            # if self.currentTurn == 1:
            #     self.currentTurn = 2
            # elif self.currentTurn == 2:
            #     self.currentTurn = 1

        return

    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

    def generateSuccessors(self, depth, computer):
        if depth >= 0 and self.pieceCount < 42:
            self.children = []
            for gameColumn in range(0, 7):

                # CHeck if it is allowed at column 'x'
                if not self.gameBoard[0][gameColumn]:

                    # Creating child nodes
                    child = maxConnect4Game()
                    child.gameBoard = copy.deepcopy(self.gameBoard)
                    if self.currentTurn == 1:
                        child.currentTurn = 2
                    elif self.currentTurn == 2:
                        child.currentTurn = 1
                    child.evaluation = 0
                    child.pieceCount = self.pieceCount + 1

                    if computer == self.currentTurn:
                        self.eval(computer)
                        # print self.bestMove["column"]
                        child.evaluation = self.bestMove["utility"]
                        child.gameBoard[self.bestMove["row"]][self.bestMove["column"]] = self.currentTurn
                        child.column = self.bestMove["column"]
                        self.children.append(child)
                        break
                    else:
                        # Finding its proper gameboard
                        for i in range(5, -1, -1):
                            if not child.gameBoard[i][gameColumn]:
                                child.gameBoard[i][gameColumn] = self.currentTurn
                                child.column = gameColumn
                                self.children.append(child)
                                break

            for child in self.children:
                child.generateSuccessors(depth - 1, computer)       
        else: 

            self.countScore()
            # Needs a change
            if computer == 1:
                self.utility = self.player1Score - self.player2Score + self.evaluation
            else:
                self.utility = self.player2Score - self.player1Score + self.evaluation
    
    def performMinMax(self, computer):
        if self.utility is not None:
            return self.utility
        elif self.currentTurn == computer:
            v = -999
            for child in self.children:
                v = max(v, child.performMinMax(computer))
        else:
            v = 999
            for child in self.children:
                v = min(v, child.performMinMax(computer))
        self.utility = v
        return self.utility

    def performAlphaBeta(self, computer, alpha, beta):
        if self.utility is not None:
            return self.utility
        elif self.currentTurn == computer:
            v = -999
            for child in self.children:
                v = max(v, child.performAlphaBeta(computer, alpha, beta))
                if alpha >= beta:
                    # Pruning occured
                    self.utility = v
                    return self.utility
                else:
                    alpha = max(alpha, v)
        else:
            v = 999
            for child in self.children:
                v = min(v, child.performAlphaBeta(computer, alpha, beta))
                if beta <= alpha:
                    # Pruning occured
                    self.utility = v
                    return self.utility
                else:
                    beta = min(v, beta)
        self.utility = v
        return self.utility

    def selectBestMove(self, computer):
        alpha = -999
        beta  = 999
        # v = self.performMinMax(computer)
        v = self.performAlphaBeta(computer, alpha, beta)
        for child in self.children:
            if child.utility == v:
                return child.column

    def eval(self, computer):
        if computer == 1:
            opposition = 2
        else:
            opposition = 1

        playableMoves = []

        # 1. Find the 7 moves I can play here
        for column in range(0, 7):
            if not self.gameBoard[0][column]:
                for row in range(5, -1, -1):
                    if not self.gameBoard[row][column]:
                        playableMoves.append({
                            "row": row,
                            "column": column
                        })
                        break
        
        if len(playableMoves) > 0:
        # 2. Compute if I can stop the opposite winning and assign self.loose
        # 3. Compute if I can win the game and assign it to self.win

            # Scars to your beautiful
            self.loose = -1
            self.win = -1
            self.probMax = -1
            self.looseBestMove = None
            self.winBestMove = None
            self.probMove = None
            self.randomMove = playableMoves[random.randrange(0, len(playableMoves))] # NEed to correct this
            for move in playableMoves:
                looseCounter = 0
                winCounter = 0
                probCounter = 0

                if move["column"] - 3 >= 0:
                    column_min = move["column"] - 3
                else:
                    column_min = 0

                if move["column"] + 3 <= 6:
                    column_max = move["column"] + 3
                else:
                    column_max = 6

                # Horizontal check
                current_row = self.gameBoard[move["row"]][:]
                current_row[move["column"]] = opposition
                for i in range(column_min, column_max - 2, 1):
                    if current_row[i:i+4] == [opposition]*4:
                        looseCounter += 1
                
                current_row[move["column"]] = computer
                for i in range(column_min, column_max - 2, 1):
                    if current_row[i:i+4] == [computer]*4:
                        winCounter += 1
                    try:
                        if current_row[i:i+4].index(opposition) >= 0:
                            pass
                    except:
                        probCounter += 1
                
                # # Vertical Check
                if move["row"] + 3 <= 5:
                    if self.gameBoard[move["row"] + 3][move["column"]] == opposition and self.gameBoard[move["row"] + 2][move["column"]] == opposition and self.gameBoard[move["row"] + 1][move["column"]] == opposition:
                        looseCounter += 1

                    if self.gameBoard[move["row"] + 3][move["column"]] == computer and self.gameBoard[move["row"] + 2][move["column"]] == computer and self.gameBoard[move["row"] + 1][move["column"]] == computer:
                        winCounter += 1

                    probArray = []
                    probArray.append(self.gameBoard[move["row"] + 3][move["column"]])
                    probArray.append(self.gameBoard[move["row"] + 2][move["column"]])
                    probArray.append(self.gameBoard[move["row"] + 1][move["column"]])
                    try:
                        if probArray.index(opposition) >= 0:
                            pass
                    except:
                        probCounter += 1
                        
                # Diagonal Right
                r_start = move["row"]
                c_start = move["column"]
                i = -3
                while i != 0 and r_start != 0 and c_start != 0:
                    r_start = r_start - 1
                    c_start = c_start - 1
                    i = i - 1

                r_end = move["row"]
                c_end = move["column"]
                i = 3
                while i != 0 and r_end != 5 and c_end != 6:
                    r_end = r_end + 1
                    c_end = c_end + 1
                    i = i - 1
                
                r_start_save = r_start
                r_end_save = r_end
                c_start_save = c_start
                c_end_save = c_end

                current_map = copy.deepcopy(self.gameBoard)
                current_map[move["row"]][move["column"]] = computer
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == computer and current_map[r_start+1][c_start+1] == computer and current_map[r_start+2][c_start+2] == computer and current_map[r_start+3][c_start+3] == computer:
                        winCounter += 1 

                    probArray = []
                    probArray.append(current_map[r_start][c_start])
                    probArray.append(current_map[r_start+1][c_start+1])
                    probArray.append(current_map[r_start+2][c_start+2])
                    probArray.append(current_map[r_start+3][c_start+3])

                    r_start = r_start + 1
                    c_start = c_start + 1

                    try:
                        if probArray.index(opposition) >= 0:
                            pass
                    except:
                        probCounter += 1
                
                r_start = r_start_save
                r_end = r_end_save
                c_start = c_start_save
                c_end = c_end_save

                current_map = copy.deepcopy(self.gameBoard)
                current_map[move["row"]][move["column"]] = opposition
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == opposition and current_map[r_start+1][c_start+1] == opposition and current_map[r_start+2][c_start+2] == opposition and current_map[r_start+3][c_start+3] == opposition:
                        looseCounter += 1 
                    r_start = r_start + 1
                    c_start = c_start + 1

                # Diagonal Left
                r_start = move["row"]
                c_start = move["column"]
                i = -3
                while i != 0 and r_start != 0 and c_start != 6:
                    r_start = r_start - 1
                    c_start = c_start + 1
                    i = i - 1

                r_end = move["row"]
                c_end = move["column"]
                i = 3
                while i != 0 and r_end != 5 and c_end != 0:
                    r_end = r_end + 1
                    c_end = c_end - 1
                    i = i - 1
                
                r_start_save = r_start
                r_end_save = r_end
                c_start_save = c_start
                c_end_save = c_end
                
                current_map = copy.deepcopy(self.gameBoard)
                current_map[move["row"]][move["column"]] = computer
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == computer and current_map[r_start+1][c_start-1] == computer and current_map[r_start+2][c_start-2] == computer and current_map[r_start+3][c_start-3] == computer:
                        winCounter += 1 

                    probArray = []
                    probArray.append(current_map[r_start][c_start])
                    probArray.append(current_map[r_start+1][c_start-1])
                    probArray.append(current_map[r_start+2][c_start-2])
                    probArray.append(current_map[r_start+3][c_start-3])

                    r_start = r_start + 1
                    c_start = c_start - 1

                    try:
                        if probArray.index(opposition) >= 0:
                            pass
                    except:
                        probCounter += 1
                
                r_start = r_start_save
                r_end = r_end_save
                c_start = c_start_save
                c_end = c_end_save
                
                current_map = copy.deepcopy(self.gameBoard)
                current_map[move["row"]][move["column"]] = opposition
                while r_start <= r_end - 3:
                    if current_map[r_start][c_start] == opposition and current_map[r_start+1][c_start-1] == opposition and current_map[r_start+2][c_start-2] == opposition and current_map[r_start+3][c_start-3] == opposition:
                        looseCounter += 1 
                    r_start = r_start + 1
                    c_start = c_start - 1

                # Final Evaluation
                if looseCounter != 0 and looseCounter > self.loose:
                    self.loose = looseCounter
                    self.looseBestMove = move

                if winCounter != 0 and winCounter > self.win:
                    self.win = winCounter
                    self.winBestMove = move

                if probCounter != 0 and probCounter > self.probMax:
                    self.probMax = probCounter
                    self.probMove = move

            # 4. Check difference between win and loose and play the move
            # 5. If both are negative, just play a move with higher possibility
            if self.win >= self.loose and self.win != -1:
                self.bestMove = {
                    "row" : self.winBestMove["row"],
                    "column" : self.winBestMove["column"],
                    "utility" : self.win * 4
                }
            elif self.win < self.loose:
                self.bestMove = {
                    "row" : self.looseBestMove["row"],
                    "column" : self.looseBestMove["column"],
                    "utility" : self.loose * 4
                }
            elif self.probMax > 0:
                self.bestMove = {
                    "row" : self.probMove["row"],
                    "column" : self.probMove["column"],
                    "utility" : self.probMax
                }
            else:
                self.bestMove = {
                    "row" : self.randomMove["row"],
                    "column" : self.randomMove["column"],
                    "utility" : 0
                }
        else:
            self.bestMove = None