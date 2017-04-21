import sys
import string
import re
from collections import Counter

fname = sys.argv[1]
k = sys.argv[2]


items = []
for line in file:
    if line.startswith('>'):
        read = file.readline()
        items.append(read)


def ReadFile(fn):
	content = ""
	with open(fn) as f:
		first_line = f.readline()
		for line in f:
			content += line.replace('\n', "")
	return content.lower()

def KmerList(dna, k):
	result = []
	for x in range(len(dna)+1-k):
		result.append(dna[x:x+k])
	return result

if __name__ == '__main__':

	# DNA sequence
	content = ReadFile(fname)
	#print(content)

	# Kmer list
	Kmers = KmerList(content, int(k))
	#print(Kmers)

	# Kmer counts
	c = Counter(Kmers)
	print(c.most_common(3))
	print(len(c))