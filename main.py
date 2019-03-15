from aligner import ChunkAligner
from chunker import HtmlChunker
import sys

def pairListToString(inputPairList):
	resultString = ""
	for i in range(len(inputPairList)):
		enChunk = inputPairList[i][0]
		koChunk = inputPairList[i][1]
		norEnChunk = inputPairList[i][2]
		norKoChunk = inputPairList[i][3]
		if(enChunk[0]==None):
			enChunk = ("None","None")
		if(koChunk[0]==None):
			koChunk = ("None","None")
		if(norEnChunk[0]==None):
			norEnChunk = ("None","None")
		if(norKoChunk[0]==None):
			norKoChunk = ("None","None")

		#resultString+= enChunk[0]+"\t"+koChunk[0]+"\n"
		resultString+= enChunk[0]+"\t"+koChunk[0]+"\t"+norEnChunk[0]+"\t"+norKoChunk[0]+"\n"
	return resultString

enChunker = HtmlChunker()
koChunker = HtmlChunker()
aligner = ChunkAligner()

enFileName = "/mnt/data/hansd410/crawled/googleCloud/95d520c1-1569-4035-8ad9-c35c72851da2"
koFileName = "/mnt/data/hansd410/crawled/googleCloud/1e755452-3e34-47a3-9e91-70afc8498f6b"
#enFileName = "/mnt/data/hansd410/crawled/googleCloud/temp_en"
#koFileName = "/mnt/data/hansd410/crawled/googleCloud/temp_ko"

#enFileName = sys.argv[1]
#koFileName = sys.argv[2]

enChunk = enChunker.chunk(enFileName)
koChunk = koChunker.chunk(koFileName)

alignedPair = aligner.align(enChunk,koChunk)
#print(alignedPair)
fout=open("log.txt","w")
fout.write(pairListToString(alignedPair))

