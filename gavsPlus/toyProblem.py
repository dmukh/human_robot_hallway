# Human-Robot Toy Problem

import sys
import random
import Tkinter as tk
from PIL import Image, ImageTk
import time

autFile = 'toyProblemFull'
simAut = 'toyProblem'

rows = 2
cols = 3
goals = 2

def createAutFile(fname):
	stateCount = 0
	with open(fname, 'w') as f:
		f.write('# Automaton for Human-Robot Hallway Toy Problem\n')
		for hLocR in xrange(0, rows):
			for hLocC in xrange(0, cols):
				for rLocR in xrange(0, rows):
					for rLocC in xrange(0, cols):
						for goal in xrange(1,goals+1):
							f.write(str(stateCount) + ' -> <hLoc:[' + str(hLocR) + ',' + str(hLocC) + '], rLoc:[' + str(rLocR) + ',' + str(rLocC) + '], goal:' + str(goal) +'>\n')
							if (rLocR==hLocR and rLocC==hLocC): #Same location
								f.write('  Successors: 73\n')
							elif rLocC==0 and hLocC==2 and ((goal==1 and hLocR==0) or (goal==2 and hLocR==1)):
								f.write('  Successors: 72\n')
							else:
								f.write('  Successors: \n')
							stateCount = stateCount + 1
		f.write(str(stateCount) + ' -> <0-sink>\n')
		stateCount = stateCount + 1
		f.write(str(stateCount) + ' -> <1-sink>\n')
		stateCount = stateCount + 1


def readAutFile(fname):
	state = []
	succ = []
	prob = []

	with open(fname, 'r') as f:
		lines = f.readlines()
		flag = 0
		for line in lines:
			if not '#' in line:
				subs = line.split()
				if flag==1 and 'Successors' in line:
					sState = []
					pState = []
					for sub in subs:
						if '(' in sub:
							ind1 = sub.index('(')
							ind2 = sub.index(')')
							sState.append(int(sub[0:ind1]))
							pState.append(float(sub[ind1+1:ind2]))
					succ.append(sState)
					prob.append(pState)
				else:
					state.append(int(subs[0]))
					flag = 1
	
	return [state, succ, prob]


if 'newAut' in sys.argv:
	createAutFile(autFile + '.aut')

if 'simulate' in sys.argv:
	out = readAutFile(simAut+'.aut')
	state = out[0]; succState = out[1]; probSucc = out[2]	

	winState = 72
	initState = 41
	
	stateSeq = []
	while winState not in stateSeq:
		if not stateSeq:
			stateSeq.append(initState)
		else:
			ind = state.index(stateSeq[-1])
			succ = succState[ind]
			prob = probSucc[ind]

			probVal = random.random()
			print probVal

			csum = 0
			for ii in range(len(prob)):
				csum = csum + prob[ii]
				if probVal < csum:
					stateSeq.append(succ[ii])
					break

	print stateSeq

