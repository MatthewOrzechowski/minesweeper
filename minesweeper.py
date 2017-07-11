import sys
import os
import subprocess
import random

class Board:
	def __init__(self, x, y, numMines):
		self.x = x
		self.y = y
		self.numMines = numMines
		self.bombs = []
		self.board = self.makeBoard(x, y, numMines)
		self.flagged = []
		self.revealQueue = []
		self.gameOver = False
		self.win = False

	def makeBoard(self, x, y, numMines):
		board = []
		for yCoor in range(y):
			row = []
			for xCoor in range(x):
				row.append(Square(xCoor, yCoor))
			board.append(row)
		i = 0
		bombs = []
		while i < numMines:
			bombX = random.randint(0, x-1)
			bombY = random.randint(0, y-1)
			if [bombX, bombY] not in bombs:
				board[bombY][bombX].isBomb = True
				self.bombs.append([bombX, bombY])
				i += 1
		for yCoor in range(y):
			for xCoor in range(x):
				board[yCoor][xCoor].value = len(self.find(xCoor, yCoor, "bombs", board))
		return board

	def makeMove(self, x, y, moveType):
		if moveType == "flag":
			if not self.board[y-1][x-1].flagged:
				self.board[y-1][x-1].flagged = True
				self.flagged.append(self.board[y-1][x-1])
				win = True
				for x in self.flagged:
					if x in self.bombs:
						win = win and False
				if win:
					self.win = True
					self.gameOver = True
			else:
				self.board[y-1][x-1].flagged = False
				self.flagged.remove(self.board[y-1][x-1])
		else:
			self.board[y-1][x-1].revealed = True
			if (self.board[y-1][x-1].isBomb):
				self.gameOver = True
			else:
				self.revealQueue = self.find(x-1, y-1, "safes")
				while len(self.revealQueue) > 0:
					square = self.revealQueue.pop()
					square.revealed = True
					self.revealQueue.extend(self.find(square.x, square.y, "safes"))

	def find(self, x, y, toFind, passedBoard=None):
		if not passedBoard:
			board = self.board
		else:
			board = passedBoard
		search = [-1, 0, 1]
		found = []
		xCoors = []
		yCoors = []
		for i in search:
			if x + i >= 0 and x + i < self.x:
				xCoors.append(x+i)
			if y + i >= 0 and y + i < self.y:
				yCoors.append(y+i)
		for yCoor in yCoors:
			for xCoor in xCoors:
				if not (x == xCoor and y == yCoor) and board[yCoor][xCoor].isBomb and toFind == "bombs":
					found.append(1)
				elif not (x == xCoor and y == yCoor) and not board[yCoor][xCoor].isBomb and not board[yCoor][xCoor].revealed and toFind == "safes":
					found.append(board[yCoor][xCoor])
		if not passedBoard:
			self.board = board
			return found
		else:
			return found

	def show(self, gameBoard):
		for row in gameBoard:
			thisRow = ""
			for item in row:
				if item.revealed and item.isBomb:
					thisRow += "* "
				elif item.revealed:
					thisRow += str(item.value) + " "
				elif item.flagged:
					thisRow += "F "
				else:
				    thisRow += "# "
			print(thisRow)
					  
class Square:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.value = -1
		self.revealed = False
		self.isBomb = False
		self.flagged = False

def clearConsole():
	if os.name in ('nt', 'dos'):
		subprocess.call('cls')
	elif os.name in ('linux', 'osx', 'posix'):
		subprocess.call('clear')
	else:
		print "\n" * 100

def getBoardInputs():
	try:
		x = input("How wide of a board would you like?: ")
		y = input("How tall of a board would you like?: ")
		numMines = input("How many mines would you like?: ")
		return [x, y, numMines]
	except NameError:
		print('Incorrect value entered, values must be positive integers')
		getBoardInputs()

def getMoveInputs():
	try:
        	move = input('Enter Move: x, y, "dig" or x, y, "flag": ')
		return move
        except NameError:
                print('Incorrect value entered: Values must be positive integers, and move must be "dig" or "flag"')
                getMoveInputs()


[x, y, numMines] = getBoardInputs()
correctType = isinstance(x, int) and isinstance(y, int) and isinstance(numMines, int)
correctValues = (x > 0 and y > 0 and numMines > 0 and numMines < x * y)
while not correctType or not correctValues:
	print("Incorrect value entered: All values must be positive integers, and the bombs must fit the board")
	[x, y, numMines] = getBoardInputs()
	correctType = isinstance(x, int) and isinstance(y, int) and isinstance(numMines, int)
	correctValues = (x > 0 and y > 0 and numMines > 0 and numMines < x * y)	

clearConsole()
print("WELCOME TO MINESWEEPER") 
print("NOTE THAT ALL COORDINATES, TO SERVE THE UNENLIGHTENED PUBLIC, ARE 1 INDEXED.")
print("THIS MEANS 1, 1 IS THE TOP LEFT CORNER")
print("\n"*2)

game = Board(x, y, numMines)
game.show(game.board)

while not game.gameOver:
	[xCoor, yCoor, moveType] = getMoveInputs()
	while not (isinstance(xCoor, int) and isinstance(yCoor, int) and isinstance(moveType, str) and xCoor > 0 and xCoor <= x and yCoor > 0 and yCoor <= y and (moveType == "dig" or moveType == "flag")):
		print('Incorrect value entered: Values must be positive integers within the dimensions of the board, and move must be "dig" or "flag"')
		[xCoor, yCoor, moveType] = getMoveInputs()
	clearConsole()
	game.makeMove(xCoor, yCoor, moveType)
	game.show(game.board)

if game.win:
	print("You win! Congratulations!")
else:
	print("Boom! Try again next time!")
