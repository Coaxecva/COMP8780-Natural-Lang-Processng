import sys
import string
import re
from collections import Counter

from nltk.tokenize import RegexpTokenizer
import nltk

iden = "(TOP END_OF_TEXT_UNIT)"

train = sys.argv[1]
test = sys.argv[2]

N_sentences = sys.argv[3]

with open(train) as f:
    content = "".join(line for line in f if not line.isspace())

#print(content)

with open(test) as f:
    content1 = "".join(line for line in f if not line.isspace())

with open(N_sentences) as f:
	text = "".join(line for line in f if not line.isspace())

tokenizer = RegexpTokenizer(r'\w+')
tokens_from_N_sentences = tokenizer.tokenize(text)

## tokens from sentences using nltk
#print(tokens_from_N_sentences)

## POS tags from nktk (groundtruth)
#print(nltk.pos_tag(tokens_from_N_sentences))

#text_ano = re.findall(r'\(([^()]+)\)', content)
#text_ano = re.findall(r'\([^\(\r\n]*\)', content)
#text_ano = [p.split(')')[0] for p in content.split('(') if ')' in p]
#print(text_ano)

#sentences = list(filter(None, content.split(iden)))
sentences = content.split(iden)
#print(sentences[0])

l_words_tags = []
####################################
# Split tags and words for training
####################################

for se in sentences:
	POS = [p.split(')')[0] for p in se.split('(') if ')' in p]
	if POS:
		t = " ".join(POS)
		#print(t)		
		for q in POS:
			l_words_tags += q.split(" ")
		#l_words_tags.append(p for p in (q.split(" ") for q in POS))

#print(l_words_tags)
words = l_words_tags[1::2]
tags = l_words_tags[0::2]


sentences1 = content1.split(iden)
l_words_tags1 = []
########################################################
# Split tags and words for testing on the Snapshot file
########################################################
for se1 in sentences1:
	POS1 = [p.split(')')[0] for p in se1.split('(') if ')' in p]
	if POS1:
		t = " ".join(POS1)
		#print(t)		
		for q in POS1:
			l_words_tags1 += q.split(" ")
		#l_words_tags.append(p for p in (q.split(" ") for q in POS))

#print(l_words_tags)
words1 = l_words_tags[1::2]
tags1 = l_words_tags[0::2]
#for i in range(len(tags1)):
#	if tags1[i] == "-NONE-":
#		del tags1[i]
#		del words1[i]

##################################################
# Hash of hashes to train a baseline lexicalized 
# statistical tagger on the entire BROWN corpus
##################################################
h = {}
for w, t in zip(words,tags):
	if w not in h:
		h[w] = {t:1}
	else:
		if t not in h[w]:
			h[w][t]=1
		else:
			h[w][t] += 1

########################################
# Tag by my tagger on the Snapshot file
########################################
my_tags1 = []
for w in words1:
	if w in h:
		tag = max(h[w], key=lambda i: h[w][i])
		my_tags1.append(tag)
	else:
		my_tags1.append("NA")

#print(tags1)
#print(my_tags1)

###################################
# Compute accuracy on 25 sentences
###################################
c = 0
for mt, t in zip(my_tags1, tags1):
	if mt == t:
		c += 1
accuracy1 = float(c)/float(len(tags1))

print("Accuracy of baseline lexicalized tagger on Snapshot file: {0}".format(accuracy1))


####################################
# Tag by my tagger for 25 sentences
####################################

my_tags = []
for w in tokens_from_N_sentences:
	if w in h:
		tag = max(h[w], key=lambda i: h[w][i])
		my_tags.append(tag)
	else: # use alternative rules
		if w.endswith("ly"):
			my_tags.append("RB")
		elif w.endswith("ive"):
			my_tags.append("JJ")
		elif w.endswith("ness") or w.endswith("ion"):
			my_tags.append("NN")
		elif w.endswith("ions") or w.endswith("ses"):
			my_tags.append("NNS")
		elif w.isnumeric():
			my_tags.append("CD")
		elif w.endswith("ing"):
			my_tags.append("VBG")
		elif w.istitle():
			my_tags.append("NNP")
		elif w.endswith("ed"):
			my_tags.append("VBN")
		else: my_tags.append("NA")

###################################
# Compute accuracy on 25 sentences
###################################
nltk_tags = [ta[1] for ta in nltk.pos_tag(tokens_from_N_sentences)]
#print(nltk_tags)
#print(my_tags)

c = 0
for mt, t in zip(my_tags, nltk_tags):
	if mt == t:
		c += 1
accuracy = float(c)/float(len(nltk_tags))

print("Accuracy of my tagger on 25 sentences: {0}".format(accuracy))