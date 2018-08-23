# Script to populate .game file
# 1. Generate .aut file
# 2. Encode .game file from .aut file

import os
import sys
import random


autFile = 'hrHall.aut'
gameFile = 'hrHall.game'
rows = 5
cols = 15
zones = 3
maxCount = 5
goals = 3

# State = [hLoc, rLoc, etGoal, count]

def getStateNum(state):
	# Convert state vector to state number in aut
	a = state[0] * ((rows*cols)*goals*(maxCount+1))
	b = state[1] * (goals*(maxCount+1))
	c = (state[2]-1) * (maxCount+1)
	d = (state[3])
	return a + b + c + d


def getStateFromNum(stateNum):
	# Convert state number to state vector
	prod = (rows*cols)*goals*(maxCount+1)
	a = stateNum / prod
	b = (stateNum - a*prod) / (prod/(rows*cols))
	c = (stateNum - a*prod - b*(prod/(rows*cols))) / (prod/((rows*cols)*goals))
	d = stateNum - a*prod - b*(prod/(rows*cols)) - c*(prod/((rows*cols)*goals))
	return [a, b, c+1, d]


def getGridLoc(gridNum):
	row = gridNum % rows
	col = gridNum/rows
	return [row, col]


def createAutFile(fname):
	stateCount = 0
	with open(fname, 'w') as f:
		f.write('# Automaton for Human-Robot Hallway Problem\n')
		for hLoc in xrange(0, rows*cols):
			for rLoc in xrange(0, rows*cols):
				for etGoal in xrange(1, goals+1):
					for count in xrange(0, maxCount+1):
						f.write(str(stateCount) + ' -> <hLoc:' + str(hLoc) + ', rLoc:' + str(rLoc) + \
							', etGoal:' + str(etGoal) + ', count:' + str(count) + '>\n')
						f.write('  Successors: \n')
						stateCount = stateCount + 1



def findSuccStates(state):
	hLoc = state[0]; rLoc = state[1]; etGoal = state[2]; count = state[3]
	
	# Next human locations
	hGrid = getGridLoc(hLoc)
	hGridNext = [[hGrid[0], hGrid[1]-1], [hGrid[0]-1, hGrid[1]], [hGrid[0]+1, hGrid[1]], [hGrid[0], hGrid[1]+1]]
	hGridNext = [h for h in hGridNext if (h[0] >= 0 and h[0] < rows and h[1] >= 0 and h[1] < cols)]
	hLocNext = [0] * len(hGridNext)
	for ii in xrange(0, len(hLocNext)):
		hLocNext[ii] = hGridNext[ii][0] + hGridNext[ii][1]*rows

	# Next robot locations
	rGrid = getGridLoc(rLoc)
	rGridNext = [[rGrid[0], rGrid[1]-1], [rGrid[0]-1, rGrid[1]], [rGrid[0]+1, rGrid[1]], [rGrid[0], rGrid[1]+1]]
	rGridNext = [r for r in rGridNext if (r[0] >= 0 and r[0] < rows and r[1] >= 0 and r[1] < cols)]
	rLocNext = [0] * len(rGridNext)
	for ii in xrange(0, len(rLocNext)):
		rLocNext[ii] = rGridNext[ii][0] + rGridNext[ii][1]*rows


	# Successor states
	succState = []
	succStateNum = []
	probSucc = []
	nextGoal = [1, 2, 3]
	for nhl in hLocNext:
		for nrl in rLocNext:
			for netgoal in nextGoal:
				nst = [nhl, nrl, netgoal, count]
				if netgoal != etGoal:
					nst[3] = count + 1

				# Check satisfiability of next state
				succState.append(nst)
				succStateNum.append(getStateNum(nst))
				if checkSafetySat(state, nst):
					probSucc.append(getProbTransition(state, nst, hLocNext, rLocNext))
				else:
					probSucc.append(0)

	return [succState, succStateNum, probSucc]



def getProbTransition(state, targetState, hGridNext, rGridNext):
	# Probability of human action

	h = .1




   
	return h * (1./3)



def checkSafetySat(state, targetState):
	hsGrid = getGridLoc(state[0])
	rsGrid = getGridLoc(state[2])
	htGrid = getGridLoc(targetState[0])
	rtGrid = getGridLoc(targetState[2])

	# safety : (isHtopU or isHfront or isHtopD -> rMoveBack) and (count <= 4)
	isHtopU = (hsGrid == [rsGrid[0]-1, rsGrid[1]-1])
	isHfront = (hsGrid == [rsGrid[0], rsGrid[1]-1])
	isHtopD = (hsGrid == [rsGrid[0]+1, rsGrid[1]-1])
	rMoveBack = (rtGrid == [rsGrid[0], rsGrid[1]+1])

	if ((not (isHtopU or isHfront or isHtopD) or rMoveBack) and (targetState[3] <= maxCount)):
		return True
	else:
		return False



def checkProgressSat(path):
	return True






# Main
if 'aut' in sys.argv:
	# Generate Automaton
	createAutFile(autFile)

	# Go through .aut file and populate successor field
	with open(autFile, 'r') as ifile, open('tmp.aut', 'w') as ofile:
		line = ifile.readline()
		num = 0
		while line:
			if '-> <hLoc:' in line:
				stateNum = int(line.split()[0])
				state = getStateFromNum(stateNum)
				succ = findSuccStates(state)
				succState = succ[0]
				succStateNum = succ[1]
				succProb = succ[2]
				ofile.write(line)
				num = num + 1
				if (num % 10000) == 0:
					print num
			elif 'Successors' in line:
				succString = ''
				for snum in succStateNum:
					rnd = random.random()
					succString = succString + str(snum) + '(' + str(rnd)[0:6] + '), '
				ofile.write('  Successors: ' + succString + '\n')
			else:
				ofile.write(line)
			line = ifile.readline()

	os.rename('tmp.aut', autFile)



if 'game' in sys.argv:
	# Generate Game File
	initState = [2, 72, 1, 0]
	initStateNum = getStateNum(initState)





	with open(gameFile, 'w') as f:
		f.write('## GAVS+ game file for Human-Robot Hallway Problem\n')
		f.write('0:1')



	print '234'

























if 'test' in sys.argv:
	initState = [2,72,1,0]

	# Test getStatNum and getStateFromNum functions - expect to print 2 True's
	num = getStateNum(initState)
	if num == 3996:
		print True
	else:
		print False

	if getStateFromNum(num) == initState:
		print True
	else:
		print False
		print getStateFromNum(num)












