#from nltk.tokenize import RegexpTokenizer
import sys
import string
import re
from collections import Counter

fname = sys.argv[1]

#tokenizer = RegexpTokenizer(r'\w+')

#text = "This is my text. It icludes commas, question marks? and other stuff. Also U.S.."
#tokens = tokenizer.tokenize(text)

with open(fname) as f:
    content = f.read().replace('\n', ' ')

content = content.lower()

#print(content)
#tokens = tokenizer.tokenize(content)

#tokens = content.translate(None, string.punctuation).split()
#tokens = content.translate(str.maketrans('','',string.punctuation)).split()
content = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", content)
tokens = content.split(" ")
tokens = [ite for ite in tokens if ite != " " and ite != '']
#print(content)
#print(tokens)

counts = Counter(tokens)
#print(counts.most_common(10))
print("The top 10 most frequent words")
for k, v in counts.most_common(10):
	print(k, ":", v)