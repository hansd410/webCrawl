import sys
import re

def listToStr(inputList):
	resultStr = ""
	for i in range(len(inputList)):
		if(i!=0):
			resultStr +="/"+ inputList[i]
		else:
			resultStr += inputList[i]
	return resultStr

class HtmlChunker:
	def chunk(self,inputFile):
		fin = open(inputFile,'r')

		# get url from first line
		url = fin.readline()
		data = fin.read()

		##################### PREPROCESS #####################
		# remove soft tags and normalize spaces
		data = re.sub("&nbsp;" ," ",data)
		#data = re.sub("< /? (?:[a-z]+:)?" + "(?:a|b|strong|i|em|font|span|nobr|sup|sub|meta|link|acronym)" + "(?:[\\s/][^>]*)? >"," ",data)
		data = re.sub("\\s+" ," ",data)

		# remove comment
		data = re.sub("<!--.*?(?:$|(?<=--)>)","",data)

		# remove inline script
		data = re.sub("<(?:script|style)(?:[^>/]+|/\\s*[^\\s>]*)*>.*?(?:$|<\\s*/\\s*(?:script|style)\\s*>)" ,"",data)

		print("whitespace processed")


		# remove short list
		#data = re.sub("<li (?:\\s[^>]*)? > \\s* .{1,100}? (?: $ | </?(?:li|ul|ol)> \\s* )" ," ",data)

		# remove short table
		#data = re.sub("<td (?:\\s[^>]*)? > \\s* .{1,100}? (?: $ | </td> \\s* )" ," ",data)

		# remove option tag
		#data = re.sub("<option (?:\\s[^>]*)? > [^<]+" ," ",data)


		##################### CHUNKER #####################
		reTag = re.compile("\\s*<[^>]+(?:>|$)\\s*")
		reText = re.compile("(?:[^<]+|<>)+")

		pos = 0
		chunkList = []


		while (pos<len(data)):
			chunkTag = reTag.match(data[pos:len(data)])
			chunkText = reText.match(data[pos:len(data)])

			# if start with tag
			if(chunkTag):
				chunk = chunkTag.group()
				pos_add = chunkTag.end()
				pos = pos+pos_add
				chunkList.append((chunk,"tag"))
			# if start with text
			elif(chunkText):
				chunk = chunkText.group()
				pos_add = chunkText.end()
				pos = pos+pos_add
				chunkList.append((chunk,"text"))
			else:
				print("can't parse"+
				data[pos:pos+100]
				)
				exit()
#			chunkList.append(chunk)
		return chunkList
