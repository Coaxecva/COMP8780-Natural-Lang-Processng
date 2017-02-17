import sys
import string
import re
from collections import Counter

iden = "(TOP END_OF_TEXT_UNIT)"

fname = sys.argv[1]

with open(fname) as f:
    content = "".join(line for line in f if not line.isspace())

#print(content)

#text_ano = re.findall(r'\(([^()]+)\)', content)
#text_ano = re.findall(r'\([^\(\r\n]*\)', content)
#text_ano = [p.split(')')[0] for p in content.split('(') if ')' in p]
#print(text_ano)

sentences = list(filter(None, content.split(iden)))

#print(sentences[0])

for se in sentences:
	if se.strip() != None:
		POS = [p.split(')')[0] for p in se.split('(') if ')' in p]
		if POS:
			print(POS)
		#print(" ".join(POS), "\n")


