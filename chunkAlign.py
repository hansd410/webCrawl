import numpy as np
import sys

def canAlignWith(e,f):
	return False

def alignmentCost(e,f):
	return 1000

enDocChunk=['a','b','c','d','e','f','g','h','i','j','k']
koDocChunk=['a','c','d','e','x','f','z','h']

flipped = False

# enDocChunk should longer
if(len(enDocChunk)<len(koDocChunk)):
	tempDocChunk = enDocChunk
	enDocChunk = koDocChunk
	koDocChunk = tempDocChunk
	flipped = True

# variable init
N = 1+len(enDocChunk)
M = 1+len(koDocChunk)
if(N==1 and M==1):
	raise NameError("two lists are empty")

MAX_DIST_OFF_DIAG = int(M*0.175)
BEAM_WIDTH = MAX_DIST_OFF_DIAG*2+1

COST_SCALE = 100
DEL_COST = 1
INS_COST = 1
SUB_SCALE = 3

OFF_LIMITS = (M+N)*COST_SCALE*max(INS_COST,max(DEL_COST,SUB_SCALE))+1

DEL = 1
INS = 2
SUB = 3

matrix = np.zeros((N,BEAM_WIDTH,2))
for beamJ in range(BEAM_WIDTH):
	matrix[0][beamJ][0]=beamJ*INS_COST
	matrix[0][beamJ][1]=INS

for i in range(N):
	diagJ = int(i*M/N)
	beamOffset = diagJ-MAX_DIST_OFF_DIAG
	beamStep = int(diagJ-((i-1)*M/N))

	# align matrix
	e = enDocChunk[i-1]

	beamJ = 0
	j=diagJ-MAX_DIST_OFF_DIAG
	prevRowBeamJ = beamJ+beamStep

	for beamJ in range(BEAM_WIDTH):
		cell=matrix[i][beamJ]
		
		if(j<0 or j>=M):
			cell[0]=OFF_LIMITS
			print("j off limits")
			j+=1
			prevRowBeamJ+=1
			continue
		elif(j==0):
			cell[0]=i*DEL_COST
			cell[1]=DEL
			print("j is zero")
			j+=1
			prevRowBeamJ+=1
			continue

		k = koDocChunk[j-1]

		delScore = 0
		insScore = 0
		subScore = 0

		if(prevRowBeamJ<BEAM_WIDTH):
			delScore = matrix[i-1][prevRowBeamJ][0]+DEL_COST*COST_SCALE
		else:
			delScore = OFF_LIMITS
		if(beamJ >0 and j>0):
			insScore = matrix[i][beamJ-1][0]+INS_COST*COST_SCALE
		else:
			insScore = OFF_IMITS
		if(prevRowBeamJ >0 and j>0 and canAlignWith(e,k)):
			subScore = matrix[i-1][prevRowBeamJ-1][0]+int(alignmentCost(e,k)*SUB_SCALE*COST_SCALE)
		else:
			subScore = OFF_LIMITS

		if(subScore < OFF_LIMITS and subScore <= delScore and subScore <= insScore):
			cell[0]=subScore
			cell[1]=SUB
		elif(delScore<OFF_LIMITS and delScore <= insScore and delScore <= subScore):
			cell[0]=delScore
			cell[1]=DEL
		elif(insScore<OFF_LIMITS):
			cell[0]=insScore
			cell[1]=INS
		else:
			cell[0]=OFF_LIMITS
		
		j+=1
		prevRowBeamJ+=1
	
		print(matrix)
		input("press enter")
	exit()

	allPairs = []
	i = N-1
	j = M-1
	diagJ = int(i*M/N)
	beamOffset = diagJ - MAX_DIST_OFF_DIAG
	beamJ = j - beamOffset

	while(i>=0 and beamJ>=0 and (i>0 or j>0)):
		cell = matrix[i][beamJ]
		enChunk = ''
		koChunk = ''
		if(cell[1]==INS):
			enChunk = None
		else:
			enChunk = enDocChunk[i-1]
		if(cell[1]==DEL):
			koChunk = None
		else:
			koChunk = koDocChunk[j-1]

		if(flipped):
			allPairs.append((koChunk,enChunk))
		else:
			allPairs.append((enChunk,koChunk))

		if(cell[1]!=INS):
			i-=1
			diagJ = int(i*M/N)
			beamOffset = diagJ-MAX_DIST_OFF_DIAG
			beamJ = j - beamOffset
		if(cell[1] != DEL):
			j-=1
			beamJ-=1

	allPairs.reverse()

# get result pair

# 
