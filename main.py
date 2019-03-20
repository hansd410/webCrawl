from aligner import ChunkAligner
from chunker import HtmlChunker
import sys
import time
import argparse

def pairListToString(inputPairList):
	resultString = ""
	for i in range(len(inputPairList)):
		if(inputPairList[i][0][1]=="tag" or inputPairList[i][1][1]=="tag"):
			continue
		enChunk = inputPairList[i][0]
		koChunk = inputPairList[i][1]
		norEnChunk = inputPairList[i][2]
		norKoChunk = inputPairList[i][3]

		resultString+= enChunk[0]+"\t"+koChunk[0]+"\n"
		#resultString+= enChunk[0]+"\t"+koChunk[0]+"\t"+norEnChunk[0]+"\t"+norKoChunk[0]+"\n"
	return resultString

def listToString(inputList):
	resultString=""
	for i in range(len(inputList)):
		if(i==0):
			resultString+=inputList[i][0]
		else:
			resultString+="\t"+inputList[i][0]
	return resultString

parser = argparse.ArgumentParser(description="align parameter")
parser.add_argument('--alignFilter',default="True",type=str,help="alignment filter")
args = parser.parse_args()

enChunker = HtmlChunker()
koChunker = HtmlChunker()
aligner = ChunkAligner()

# google cloud
#enFileName = "/mnt/data/hansd410/crawled/googleCloud/e275d6e0-a325-41bb-9077-8f7e3c4ecee3"
#koFileName = "/mnt/data/hansd410/crawled/googleCloud/20596c5a-de63-4e17-ad3c-c22e0b4da46e"
# chromeEnterprise
#enFileName = "/mnt/data/hansd410/crawled/googleCloud/85985828-9d33-426b-9310-efa57513f91e"
#koFileName = "/mnt/data/hansd410/crawled/googleCloud/9e7fd013-efaa-4756-9b14-35c4bdd3b2ee"
# IoT
enFileName = "/mnt/data/hansd410/crawled/googleCloud/efc7bd3c-4c33-4cad-bdf4-3bd2bc6d4e03"
koFileName = "/mnt/data/hansd410/crawled/googleCloud/63ac5c9b-b15e-4d23-8d1b-3463bf91b8ef"

#enFileName = sys.argv[1]
#koFileName = sys.argv[2]

start_time = time.time()

enChunk = enChunker.chunk(enFileName)
koChunk = koChunker.chunk(koFileName)
print("enChunk len : "+str(len(enChunk)))
print("koChunk len : "+str(len(koChunk)))

alignedPair = aligner.align(enChunk,koChunk,args.alignFilter)
end_time = time.time()
print("whole time : "+str(end_time-start_time)+" sec")
#print(alignedPair)
#fout=open("data/googleCloud.txt","w")
#fout=open("data/enterprise.txt","w")
fout=open("data/iot.txt","w")
fout.write(pairListToString(alignedPair))

