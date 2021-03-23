import sys, random, math, copy
from typing import List, Dict


TIE_ORDER = ['U', 'R', 'D', 'L'] #for P, B, and D
DONT_HIT = ['P', 'B', 'D', 'R']
lose = False
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

#stores all initial treasure to an array
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

	#helpful class function to see description of character
	def description(self):
		return f"{self.name} is at {self.posx}, {self.posy} pointing {self.direction} and can move {self.options}"


#prints the board
def printBoard(s) -> str:
	gameBoard = ""
	for i in range(int(boardSize[0])):
		for j in range(int(boardSize[1])):
			gameBoard += s["board"][i][j]
		if i != int(boardSize[0])-1:
			gameBoard += "\n"
	return gameBoard


#places treasure back on board
def updateBoard(s) -> None:
	for i in range(len(s["treasure"])):
		for j in range(len(s["treasure"][i])):
			row = s["treasure"][i][j][0]
			col = s["treasure"][i][j][1]
			if s["board"][row][col] not in DONT_HIT:
				if s["board"][row][col] != 'A':
					if i == 0:
						s["board"][row][col] = '.'
					elif i == 1:
						s["board"][row][col] = '$'
					else:
						s["board"][row][col] = '*'

#finds indices of char on board
def findChar(char: str) -> List[int]:
	for i in range(int(boardSize[0])):
		for j in range(int(boardSize[1])):
			if board[i][j] == char:
				return [i, j]

#finds all of the possible moves for each character
def getPossibleMoves(s, character) -> None:
	character.options = ['U', 'R', 'D', 'L']
	ghosts = []
	#check up
	if character.posx > 1:
		if s["board"][character.posx-1][character.posy] == '#':
			character.options.remove('U')
	else:
		character.options.remove('U')

	#check down
	if character.posx < int(boardSize[0])-1:
		if s["board"][character.posx+1][character.posy] == '#':
			character.options.remove('D')
	else:
		character.options.remove('D')

	#check left
	if character.posy > 1:
		if s["board"][character.posx][character.posy-1] == '#':
			character.options.remove('L')
	else:
		character.options.remove('L')

	#check right
	if character.posy < int(boardSize[1])-1:
		if s["board"][character.posx][character.posy+1] == '#':
			character.options.remove('R')
	else:
		character.options.remove('R')

#moves actman
def moveActman(s, actman, punky, bunky, dunky, runky) -> bool:
	positions = [[punky.posx,punky.posy],[bunky.posx,bunky.posy],[dunky.posx,dunky.posy],[runky.posx,runky.posy]]
	move1(s, actman)
	#if actman is on a ghost, lose
	if [actman.posx,actman.posy] in positions:
		s["board"][actman.posx][actman.posy] = 'X'
		#lose()
		return False
	#else, update board with actman position
	s["board"][actman.posx][actman.posy] = 'A'
	return True

#removes treasure if found at actman position before move
def checkTreasure(s, character, positions) -> None:
	symbols = ['.', '$', '*']
	#if the character position is a treasure
	if character.name == "Act-Man" and [character.posx, character.posy] not in positions:
		for i in range(len(s["treasure"])):
			#add points based on what treasure actman is on
			if [character.posx, character.posy] in s["treasure"][i]:
				if i == 0:
					s["score"] += 1
				elif i == 1:
					s["score"] += 5
				else:
					s["score"] += 10
				#remove treasure from board after collected
				s["treasure"][i].remove([character.posx, character.posy])
	updateBoard(s)

#adds treasure back to board if a ghost
def addTreasure(s, character) -> None:
	if character.name != "Act-Man":
		#check which key has the value of the position
		if [character.posx, character.posy] in s["treasure"][0]:
			s["board"][character.posx][character.posy] = '.'
		elif [character.posx, character.posy] in s["treasure"][1]:
			s["board"][character.posx][character.posy] = '$'
		elif [character.posx, character.posy] in s["treasure"][2]:
			s["board"][character.posx][character.posy] = '*'

#moves character 1 space and deals with treasures
def move1(s, character) -> None:
	newList = []
	#get a list of all characters that isn't moving character
	for i in DONT_HIT:
		if i != character.name:
			newList.append(i)

	#check if first option is up
	if character.options[0] == 'U':
		#if actman, just add direction to moves
		if character.name == "Act-Man":
			s["moves"] += "U"
		#if current spot doesn't have a character in it, set it equal to a space
		if s["board"][character.posx][character.posy] not in newList:
			s["board"][character.posx][character.posy] = ' '
		#add treasure back to board
		addTreasure(s, character)
		#move character position
		character.posx -= 1
		#put character letter on board if not actman
		if character.name != "Act-Man":
			s["board"][character.posx][character.posy] = character.name
	#check if first option is right
	elif character.options[0] == 'R':
		if character.name == "Act-Man":
			s["moves"] += "R"
		if s["board"][character.posx][character.posy] not in newList:
			s["board"][character.posx][character.posy] = ' '
		addTreasure(s, character)
		character.posy += 1
		if character.name != "Act-Man":
			s["board"][character.posx][character.posy] = character.name
	#check if first option is down
	elif character.options[0] == 'D':
		if character.name == "Act-Man":
			s["moves"] += "D"
		if s["board"][character.posx][character.posy] not in newList:
			s["board"][character.posx][character.posy] = ' '
		addTreasure(s, character)
		character.posx += 1
		if character.name != "Act-Man":
			s["board"][character.posx][character.posy] = character.name
	#first option is left
	else:
		if character.name == "Act-Man":
			s["moves"] += "L"
		if s["board"][character.posx][character.posy] not in newList:
			s["board"][character.posx][character.posy] = ' '
		addTreasure(s, character)
		character.posy -= 1
		if character.name != "Act-Man":
			s["board"][character.posx][character.posy] = character.name
	#update direction
	character.direction = character.options[0]

def getOrderedList(character, newList) -> List[str]:
	optionsList = []
	#orders character options based on URDL order
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

def checkFirstTwo(s, character) -> bool:
	#if theres only one move
	if len(character.options) == 1:
		move1(s, character)
		s["board"][character.posx][character.posy] = character.name
	#checks if punky has 2 options, check for opposite direction
	elif len(character.options) == 2:
		for i in range(len(TIE_ORDER)):
			if TIE_ORDER[i] == character.options[0]:
				#if the first option is opposite of direction
				if TIE_ORDER[(i+2)%4] == character.direction:
					character.options.pop(0)
				move1(s, character)
				s["board"][character.posx][character.posy] = character.name
				break
	else:
		return False
	return True

#gets move for punky
def movePunky(s, punky, actman) -> None:
	getPossibleMoves(s, punky)
	if not checkFirstTwo(s, punky):
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
		
		#get the smallest distance values
		smallest = min(distances.values())
		newList = []
		#add moves to newList with smallest distance values
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)

		punky.options = getOrderedList(punky, newList)
		
		move1(s, punky)

def moveBunky(s, bunky, actman) -> None:
	getPossibleMoves(s, bunky)
	if not checkFirstTwo(s, bunky):
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
		
		#get the smallest distance values
		smallest = min(distances.values())
		newList = []
		#add moves to newList with smallest distance values
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)
		bunky.options = getOrderedList(bunky, newList)
		
		move1(s, bunky)


def moveDunky(s, dunky, actman) -> None:
	getPossibleMoves(s, dunky)
	goal = dTargets[s["dunkyIndex"]]
	goal[0] = int(goal[0])
	goal[1] = int(goal[1])

	if((dunky.posx == goal[0]) and (dunky.posy == goal[1])):
		if s["dunkyIndex"]+1 > 3:
			s["dunkyIndex"] = 0
		else:
			s["dunkyIndex"] += 1
	if not checkFirstTwo(s, dunky):

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
		
		#get the smallest distance values
		smallest = min(distances.values())
		newList = []
		#add moves to newList with smallest distance values
		for key, value in distances.items():
			if float(value) == smallest:
				newList.append(key)

		dunky.options = getOrderedList(dunky, newList)
		
		move1(s, dunky)


def moveRunky(s, runky, actman) -> None:
	getPossibleMoves(s, runky)

	newList = []
	if not checkFirstTwo(s, runky):
		#find next feasible move in runky move list
		for i in range(s["runkyIndex"],s["runkyIndex"]+len(rMoves)):
			if rMoves[i%len(rMoves)] in runky.options:
				runky.options[0] = rMoves[i%len(rMoves)]
				move1(s, runky)
				break
			#if at last index, set back equal to first index
			if s["runkyIndex"] == len(rMoves)-1:
				s["runkyIndex"] = 0
			else: #increment runky's index
				s["runkyIndex"] += 1
		if s["runkyIndex"] == len(rMoves)-1:
			s["runkyIndex"] = 0
		else:
			s["runkyIndex"] += 1


#checks for winning score
def goal(s) -> bool:
	if s["score"] >= 24:
		return True
	return False


#just runs the game
def transitionFunction(s) -> Dict[str,any]:
	#if able to move actman without losing (makes game faster)
	if moveActman(s, s["actMan"], s["punky"], s["bunky"], s["dunky"], s["runky"]):
		movePunky(s, s["punky"], s["actMan"])
		moveBunky(s, s["bunky"], s["actMan"])
		moveDunky(s, s["dunky"], s["actMan"])
		moveRunky(s, s["runky"], s["actMan"])
		positions = [[s["punky"].posx,s["punky"].posy],[s["bunky"].posx,s["bunky"].posy],[s["dunky"].posx,s["dunky"].posy],[s["runky"].posx,s["runky"].posy]]
		checkTreasure(s, s["actMan"], positions)
	else:
		s["lose"] = True
	return s


#heuristic function that returns priority-queue based on moves with highest scores
def h(boardList) -> List[Dict[str,any]]:
	return sorted(boardList, key = lambda i: i["score"], reverse=True)


def BestFS_helper(px, newBoard, direction) -> List[Dict[str,any]]:
	board1 = copy.deepcopy(newBoard)
	board1["actMan"].options = direction
	sx = transitionFunction(board1)
	#if actman doesn't lose, add the board to px
	if sx["lose"] == False:
		px.append(sx)
	return px


def BestFS(frontier) -> Dict[str,any]:
	newBoard = {}

	while frontier:
		newBoard = copy.deepcopy(frontier[0])
		frontier.pop(0)

		#if reached winning score, return current board
		if goal(newBoard):
			return newBoard

		#finds actman's next possible moves on current board
		getPossibleMoves(newBoard, newBoard["actMan"])
		#goes through all possible moves and and adds corresponding new boards to frontier
		px = []
		if 'R' in newBoard["actMan"].options:
			px = BestFS_helper(px, newBoard, ['R'])
			
		if 'D' in newBoard["actMan"].options:
			px = BestFS_helper(px, newBoard, ['D'])
					
		if 'L' in newBoard["actMan"].options:
			px = BestFS_helper(px, newBoard, ['L'])

		if 'U' in newBoard["actMan"].options:
			px = BestFS_helper(px, newBoard, ['U'])

		#calls heuristic function
		px = h(px)
		#adds px to frontier
		for i in px:
			frontier.append(i)

	#returns the newest board if frontier empty
	return newBoard


def main() -> None:
	#initialize all of the characters
	actMan = Character("Act-Man", None, findChar('A')[0], findChar('A')[1], None)
	punky = Character("P", startDirs[0], findChar('P')[0], findChar('P')[1], None)
	bunky = Character("B", startDirs[1], findChar('B')[0], findChar('B')[1], None)
	dunky = Character("D", startDirs[2], findChar('D')[0], findChar('D')[1], None)
	runky = Character("R", startDirs[3], findChar('R')[0], findChar('R')[1], None)

	#Dictionary that holds all of variables to store an instance of the game board
	gameBoard = {}
	for var in ["lose","treasure","dunkyIndex","runkyIndex","score","board","moves","actMan",
	"punky","bunky","dunky","runky"]:
		gameBoard[var] = eval(var)

	#call the Greed Best-First Search
	winningBoard = BestFS([gameBoard])

	#write the output to file
	r = open(sys.argv[2],"w")
	r.write(str(winningBoard["moves"]) + '\n')
	r.write(str(winningBoard["score"]) + '\n')
	r.write(printBoard(winningBoard))


if __name__ == "__main__":
	main()
