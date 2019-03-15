import numpy as np
import sys
import re
import math

def getAnchor(chunk):
	reAnchor = re.compile("\\b\\d+\\b")
	anchorList = reAnchor.findall(chunk)
	return '\\0'.join(anchorList)

def tagNormalize(chunk):
	reNormalize = re.compile("(?<=\\w)[^\\w>][^>]*")
	if(chunk[0]!=None):
		chunk=(reNormalize.sub('',chunk[0].lower().strip()), chunk[1])
	return chunk

def canAlignWith(e,k):
	if(e[1]==k[1]):
		if(e[1]=="text"):
			return True
		else:
			# normalize using regex
			e_normal = tagNormalize(e)
			k_normal = tagNormalize(k)
			if(e_normal[0]==k_normal[0]):
				return True
	return False

def alignmentCost(e,k):
	if(e[1]=="text" and k[1]=="text"):
		if(getAnchor(e[0])!=getAnchor(k[0])):
			return 1
		else:
			if(len(e[0])>len(k[0])):
				return math.log((25.0+len(k[0]))/(25.0+len(e[0])))
			else:
				return math.log((25.0+len(e[0]))/(25.0+len(k[0])))
	else:
		return 0


class ChunkAligner:

	def align(self, enDocChunk, koDocChunk):
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

		wholeMatrix = -np.ones((N,M,2))
		matrix = np.zeros((N,BEAM_WIDTH,2))
		for beamJ in range(BEAM_WIDTH):
			matrix[0][beamJ][0]=beamJ*INS_COST
			matrix[0][beamJ][1]=INS

		for i in range(1,N):
			diagJ = int(i*M/N)
			beamOffset = diagJ-MAX_DIST_OFF_DIAG
			beamStep = int(diagJ-((i-1)*M/N))

			# align matrix
			e = enDocChunk[i-1]

			beamJ = 0
			j=diagJ-MAX_DIST_OFF_DIAG
			# modified
			prevRowBeamJ = beamJ-beamStep

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
					wholeMatrix[i][j][0]=cell[0]
					wholeMatrix[i][j][1]=cell[1]
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
					insScore = OFF_LIMITS
				if(prevRowBeamJ >0 and j>0 and canAlignWith(e,k)):
					subScore = matrix[i-1][prevRowBeamJ-1][0]+int(alignmentCost(e,k)*SUB_SCALE*COST_SCALE)
				else:
					subScore = OFF_LIMITS

#				print("index")
#				print(i)
#				print(beamJ)
#				print("Score")
#				print(delScore)
#				print(insScore)
#				print(subScore)
#				exit()
				if(subScore < OFF_LIMITS and subScore <= delScore and subScore <= insScore):
					cell[0]=subScore
					cell[1]=SUB
					wholeMatrix[i][j][0]=cell[0]
					wholeMatrix[i][j][1]=cell[1]

				elif(delScore<OFF_LIMITS and delScore <= insScore and delScore <= subScore):
					cell[0]=delScore
					cell[1]=DEL
					wholeMatrix[i][j][0]=cell[0]
					wholeMatrix[i][j][1]=cell[1]

				elif(insScore<OFF_LIMITS):
					cell[0]=insScore
					cell[1]=INS
					wholeMatrix[i][j][0]=cell[0]
					wholeMatrix[i][j][1]=cell[1]

				else:
					cell[0]=OFF_LIMITS
					wholeMatrix[i][j][0]=cell[0]

				
				j+=1
				prevRowBeamJ+=1
			
		allPairs = []
		i = N-1
		j = M-1
		diagJ = int(i*M/N)
		beamOffset = diagJ - MAX_DIST_OFF_DIAG
		beamJ = j - beamOffset

		while(i>=0 and beamJ>=0 and (i>0 or j>0)):
			# out of bound case
			while(beamJ >= matrix.shape[1]):
				beamJ -=1
			cell = matrix[i][beamJ]
			enChunk = ''
			koChunk = ''
			if(cell[1]==INS):
				enChunk = (None,None)
			else:
				enChunk = enDocChunk[i-1]
			if(cell[1]==DEL):
				koChunk = (None,None)
			else:
				koChunk = koDocChunk[j-1]

			if(flipped):
				allPairs.append((koChunk,enChunk,tagNormalize(koChunk),tagNormalize(enChunk)))
			else:
				allPairs.append((enChunk,koChunk,tagNormalize(enChunk),tagNormalize(koChunk)))

			if(cell[1]!=INS):
				i-=1
				diagJ = int(i*M/N)
				beamOffset = diagJ-MAX_DIST_OFF_DIAG
				beamJ = j - beamOffset
			if(cell[1] != DEL):
				j-=1
				beamJ-=1
		#np.savetxt('matrix.txt',wholeMatrix[:,:,0],fmt='%.2e')
		#np.savetxt('matrix_inst.txt',wholeMatrix[:,:,1],fmt='%.2e')
		allPairs.reverse()
		return allPairs

		# get result pair

