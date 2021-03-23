'''
order of moves:
1. Act-man move
2. Check cells for same position as ghosts
3. Punky, Bunky, Dunky, Runky make moves in order
4. Check cells for same positions
5. collect treasure if any at current location

Movement of ghosts:
a). if only one move available, ghost makes move
b). ***** if 2 valid moves available, ghost moves NOT opposite to currect direction *****
c). ***** > 2 moves available, its based on personality *****


Personality:

(P)Punky (Chaser):
- makes move that is closest to act-man
- tie order: [up, right, down, left]

(B)Bunky (interceptor):
- target cell (4 spaces ahead of act-man based on his current location and direction)
- target cell can be outside of dungeon
- moves to adjacent cell that is closest to target cell
- tie order: [up, right, down, left]

(D)Dunky (Patroller):
- has 4 random target locations (have to be open)
- makes move that is closest to first target location
- if at target location, moves on to next target location
- tie order: [up, right, down, left]

(R)Runky (Random):
- has a list of random pre-generated moves
- moves to next valid move in list
- if at last move in list, circle back to start


Act-man:
- random but valid sequence of actions
- valid: moves from currect cell to open adjacent space
- game end: game-over, victory, or moves = 10


Input (in order):
1. rows (R), columns (C)
2. game board dungeon:
	- ' ' = space
	- '#' = wall
	- '.' = nugget
	- '$' = bar
	- '*' = diamond
	- 'A' = act-man
	- 'P' = Punky
	- 'B' = Bunky
	- 'D' = Dunky
	- 'R' = Runky
3. 4 char string of moves for each ghost in order (P, B, D, R)
4. int n followed by n coordinates for D's target locations
5. string of moves for R's move list
EX:
5 11
###########
#...#P...B#
#A#.$.###*#
#...#D...R#
###########
UUDD
2 1 1 3 9
UULRDD


Output (in order):
1. sequence of valid moves executed by Act-Man
2. int score (points from gold / diamonds)
3. final configuration of game board 
	- if act-man is dead put 'X'
	- if two ghosts take up same space, show whoever moves last
EX:
URRLLDUDDR
5
###########
# #D...R#
# #.$.###*#
# A.#P...B#
###########

'''
import sys, random, math
from typing import List


TIE_ORDER = ['U', 'R', 'D', 'L'] #for P, B, and D
DONT_HIT = ['P', 'B', 'D', 'R']
treasure = [[],[],[]]
dunkyIndex = 0
runkyIndex = 0
score = 0

board = []
moves = ""

f = open(sys.argv[1])
readIn = f.readlines()
boardSize = readIn[0].split()

for i in range(1, int(boardSize[0])+1):
	row = readIn[i].split()
	board.append(list(row[0]))

startDirs = readIn[int(boardSize[0])+1].strip('\n')
dTargetStr = readIn[int(boardSize[0])+2].split()
rMoves = readIn[int(boardSize[0])+3].strip('\n')

dTargets = []
for i in range(1,int(dTargetStr[0])+1):
	dTargets.append([dTargetStr[i*2-1],dTargetStr[i*2]])

for i in range(int(boardSize[0])):
	for j in range(int(boardSize[1])):
		if board[i][j] == '.':
			treasure[0].append([i, j])
		if board[i][j] == '$':
			treasure[1].append([i, j])
		if board[i][j] == '*':
			treasure[2].append([i, j])

class Character:
	#constructor
	def __init__(self, name, direction, posx, posy, options):
		self.name = name
		self.direction = direction
		self.posx = posx
		self.posy = posy
		self.options = options

	def description(self):
		return f"{self.name} is at {self.posx}, {self.posy} pointing {self.direction} and can move {self.options}"



def printBoard() -> str:
	gameBoard = ""
	for i in range(int(boardSize[0])):
		for j in range(int(boardSize[1])):
			gameBoard += board[i][j]
		if i != int(boardSize[0])-1:
			gameBoard += "\n"
	return gameBoard

def updateBoard() -> None:
	for i in range(len(treasure)):
		for j in range(len(treasure[i])):
			row = treasure[i][j][0]
			col = treasure[i][j][1]
			if board[row][col] not in DONT_HIT:
				if board[row][col] != 'A':
					if i == 0:
						board[row][col] = '.'
					elif i == 1:
						board[row][col] = '$'
					else:
						board[row][col] = '*'

def lose() -> None:
	global moves, score
	r = open(sys.argv[2],"w")
	r.write(str(moves) + '\n')
	r.write(str(score) + '\n')
	r.write(printBoard())
	#print(moves)
	#print(score)
	#printBoard()
	sys.exit()

#finds indices of char on board
def findChar(char: str) -> List[int]:
	for i in range(int(boardSize[0])):
		for j in range(int(boardSize[1])):
			if board[i][j] == char:
				return [i, j]

#finds all of the possible moves for each character
def getPossibleMoves(character) -> None:
	character.options = ['U', 'R', 'D', 'L']
	ghosts = []
	#check up
	if character.posx > 1:
		if board[character.posx-1][character.posy] == '#':
			character.options.remove('U')
	else:
		character.options.remove('U')

	#check down
	if character.posx < int(boardSize[0])-1:
		if board[character.posx+1][character.posy] == '#':
			character.options.remove('D')
	else:
		character.options.remove('D')

	#check left
	if character.posy > 1:
		if board[character.posx][character.posy-1] == '#':
			character.options.remove('L')
	else:
		character.options.remove('L')

	#check right
	if character.posy < int(boardSize[1])-1:
		if board[character.posx][character.posy+1] == '#':
			character.options.remove('R')
	else:
		character.options.remove('R')

#moves actman
def moveActman(actman, punky, bunky, dunky, runky) -> None:
	positions = [[punky.posx,punky.posy],[bunky.posx,bunky.posy],[dunky.posx,dunky.posy],[runky.posx,runky.posy]]
	getPossibleMoves(actman)
	random.shuffle(actman.options)
	move1(actman)
	if [actman.posx,actman.posy] in positions:
		board[actman.posx][actman.posy] = 'X'
		lose()
	board[actman.posx][actman.posy] = 'A'

#removes treasure if found at actman position before move
def checkTreasure(character, positions) -> None:
	global score
	symbols = ['.', '$', '*']
	#if the character position is a treasure
	if character.name == "Act-Man" and [character.posx, character.posy] not in positions:
		for i in range(len(treasure)):
			if [character.posx, character.posy] in treasure[i]:
				if i == 0:
					score += 1
				elif i == 1:
					score += 5
				else:
					score += 10
				treasure[i].remove([character.posx, character.posy])
	updateBoard()

#adds treasure back to board if a ghost
def addTreasure(character) -> None:
	if character.name != "Act-Man":
		#check which key has the value of the position
		if [character.posx, character.posy] in treasure[0]:
			board[character.posx][character.posy] = '.'
		elif [character.posx, character.posy] in treasure[1]:
			board[character.posx][character.posy] = '$'
		elif [character.posx, character.posy] in treasure[2]:
			board[character.posx][character.posy] = '*'

#moves character 1 space and deals with treasures
def move1(character) -> None:
	global moves
	newList = []
	for i in DONT_HIT:
		if i != character.name:
			newList.append(i)

	if character.options[0] == 'U':
		if character.name == "Act-Man":
			moves += "U"
		if board[character.posx][character.posy] not in newList:
			board[character.posx][character.posy] = ' '
		addTreasure(character)
		character.posx -= 1
		#checkTreasure(character)
		if character.name != "Act-Man":
			board[character.posx][character.posy] = character.name
	elif character.options[0] == 'R':
		if character.name == "Act-Man":
			moves += "R"
		if board[character.posx][character.posy] not in newList:
			board[character.posx][character.posy] = ' '
		addTreasure(character)
		character.posy += 1
		#checkTreasure(character)
		if character.name != "Act-Man":
			board[character.posx][character.posy] = character.name
	elif character.options[0] == 'D':
		if character.name == "Act-Man":
			moves += "D"
		if board[character.posx][character.posy] not in newList:
			board[character.posx][character.posy] = ' '
		addTreasure(character)
		character.posx += 1
		#checkTreasure(character)
		if character.name != "Act-Man":
			board[character.posx][character.posy] = character.name
	else:
		if character.name == "Act-Man":
			moves += "L"
		if board[character.posx][character.posy] not in newList:
			board[character.posx][character.posy] = ' '
		addTreasure(character)
		character.posy -= 1
		#checkTreasure(character)
		if character.name != "Act-Man":
			board[character.posx][character.posy] = character.name
	character.direction = character.options[0]

def getOrderedList(character, newList) -> List[str]:
	optionsList = []
	if len(newList) > 1:
		if 'U' in newList:
			optionsList.append('U')
		if 'R' in newList:
			optionsList.append('R')
		if 'D' in newList:
			optionsList.append('D')
		if 'L' in newList:
			optionsList.append('L')
	else:
		optionsList = newList

	return optionsList

def checkFirstTwo(character) -> bool:
	#if theres only one move
	if len(character.options) == 1:
		move1(character)
		board[character.posx][character.posy] = character.name
	#checks if punky has 2 options, check for opposite direction
	elif len(character.options) == 2:
		for i in range(len(TIE_ORDER)):
			if TIE_ORDER[i] == character.options[0]:
				#if the first option is opposite of direction
				if TIE_ORDER[(i+2)%4] == character.direction:
					character.options.pop(0)
				move1(character)
				board[character.posx][character.posy] = character.name
				break
	else:
		return False
	return True

#gets move for punky
def movePunky(punky, actman) -> None:
	getPossibleMoves(punky)
	if not checkFirstTwo(punky):
		distances = {}
		for i in range(len(punky.options)):
			distances[punky.options[i]] = 0.0 #set each option equal to 0 initially
			#if the option is 'U' find distance from punky up 1 to act-man
			if punky.options[i] == 'U':
				distances['U'] += math.sqrt(abs(punky.posx-1-actman.posx)**2 + abs(punky.posy-actman.posy)**2)
			elif punky.options[i] == 'R':
				distances['R'] += math.sqrt(abs(punky.posx-actman.posx)**2 + abs(punky.posy+1-actman.posy)**2)
			elif punky.options[i] == 'D':
				distances['D'] += math.sqrt(abs(punky.posx+1-actman.posx)**2 + abs(punky.posy-actman.posy)**2)
			else:
				distances['L'] += math.sqrt(abs(punky.posx-actman.posx)**2 + abs(punky.posy-1-actman.posy)**2)
		
		smallest = min(distances.values())
		newList = []
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)

		punky.options = getOrderedList(punky, newList)
		
		move1(punky)

def moveBunky(bunky, actman) -> None:
	getPossibleMoves(bunky)
	if not checkFirstTwo(bunky):
		#direction +4
		x = 0
		y = 0
		if actman.direction == 'U':
			x = -4
		elif actman.direction == 'R':
			y = 4
		elif actman.direction == 'D':
			x = 4
		else:
			y = -4

		distances = {}
		for i in range(len(bunky.options)):
			distances[bunky.options[i]] = 0.0 #set each option equal to 0 initially
			#if the option is 'U' find distance from punky up 1 to act-man
			if bunky.options[i] == 'U':
				distances['U'] = math.sqrt(abs(((bunky.posx-1)-(actman.posx+x))**2) + abs((bunky.posy-(actman.posy+y))**2))
			elif bunky.options[i] == 'R':
				distances['R'] = math.sqrt(abs((bunky.posx-(actman.posx+x))**2) + abs(((bunky.posy+1)-(actman.posy+y))**2))
			elif bunky.options[i] == 'D':
				distances['D'] = math.sqrt(abs(((bunky.posx+1)-(actman.posx+x))**2) + abs((bunky.posy-(actman.posy+y))**2))
			else:
				distances['L'] = math.sqrt(abs((bunky.posx-(actman.posx+x))**2) + abs(((bunky.posy-1)-(actman.posy+y))**2))
		smallest = min(distances.values())
		newList = []
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)
		bunky.options = getOrderedList(bunky, newList)
		
		move1(bunky)


def moveDunky(dunky, actman) -> None:
	global dunkyIndex
	getPossibleMoves(dunky)
	goal = dTargets[dunkyIndex]
	goal[0] = int(goal[0])
	goal[1] = int(goal[1])

	if((dunky.posx == goal[0]) and (dunky.posy == goal[1])):
		if dunkyIndex+1 > 3:
			dunkyIndex = 0
		else:
			dunkyIndex += 1
	if not checkFirstTwo(dunky):

		distances = {}
		for i in range(len(dunky.options)):
			distances[dunky.options[i]] = 0.0 #set each option equal to 0 initially
			#if the option is 'U' find distance from punky up 1 to act-man
			if dunky.options[i] == 'U':
				distances['U'] += math.sqrt(abs((dunky.posx-1)-int(goal[0]))**2 + abs(dunky.posy-int(goal[1]))**2)
			elif dunky.options[i] == 'R':
				distances['R'] += math.sqrt(abs(dunky.posx-int(goal[0]))**2 + abs((dunky.posy+1)-int(goal[1]))**2)
			elif dunky.options[i] == 'D':
				distances['D'] += math.sqrt(abs((dunky.posx+1)-int(goal[0]))**2 + abs(dunky.posy-int(goal[1]))**2)
			else:
				distances['L'] += math.sqrt(abs(dunky.posx-int(goal[0]))**2 + abs((dunky.posy-1)-int(goal[1]))**2)
		
		smallest = min(distances.values())
		newList = []
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)

		dunky.options = getOrderedList(dunky, newList)
		
		move1(dunky)


def moveRunky(runky, actman) -> None:
	global runkyIndex
	getPossibleMoves(runky)

	newList = []
	if not checkFirstTwo(runky):
		#find next feasible move in runky move list
		for i in range(runkyIndex,runkyIndex+len(rMoves)):
			if rMoves[i%len(rMoves)] in runky.options:
				runky.options[0] = rMoves[i%len(rMoves)]
				move1(runky)
				break
			if runkyIndex == len(rMoves)-1:
				runkyIndex = 0
			else:
				runkyIndex += 1
		if runkyIndex == len(rMoves)-1:
			runkyIndex = 0
		else:
			runkyIndex += 1

def main() -> None:
	
	actMan = Character("Act-Man", None, findChar('A')[0], findChar('A')[1], None)
	punky = Character("P", startDirs[0], findChar('P')[0], findChar('P')[1], None)
	bunky = Character("B", startDirs[1], findChar('B')[0], findChar('B')[1], None)
	dunky = Character("D", startDirs[2], findChar('D')[0], findChar('D')[1], None)
	runky = Character("R", startDirs[3], findChar('R')[0], findChar('R')[1], None)

	
	#i = 0
	while True:
		win = True
		moveActman(actMan, punky, bunky, dunky, runky)
		movePunky(punky,actMan)
		moveBunky(bunky,actMan)
		moveDunky(dunky,actMan)
		moveRunky(runky,actMan)
		positions = [[punky.posx,punky.posy],[bunky.posx,bunky.posy],[dunky.posx,dunky.posy],[runky.posx,runky.posy]]
		checkTreasure(actMan, positions)
		positions = [[punky.posx,punky.posy],[bunky.posx,bunky.posy],[dunky.posx,dunky.posy],[runky.posx,runky.posy]]
		if [actMan.posx, actMan.posy] in positions:
			lose()
		#checks if all treasure is found
		for j in treasure:
			if j:
				win = False
				break
		if win:
			break

		#i += 1


	r = open(sys.argv[2],"w")
	r.write(str(moves) + '\n')
	r.write(str(score) + '\n')
	r.write(printBoard())
	#print(moves)
	#print(score)
	#printBoard()



if __name__ == "__main__":
	main()