import re
import sys

def getAnchor(chunk):
	reAnchor = re.compile("\\b\\d+\\b")
	#anchorTag = reAnchor.match(chunk)
	anchorTag=reAnchor.findall(chunk)
	return '\\0'.join(anchorTag)
	#return (anchorTag.findall())

#getAnchor(sys.argv[1])
print(getAnchor(sys.argv[1]))

