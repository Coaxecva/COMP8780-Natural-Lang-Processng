import sys
import string
import re
from collections import Counter

iden = "(TOP END_OF_TEXT_UNIT)"

tagset = ["S","CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","PRP$","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WP$","WRB"]


input_file = sys.argv[1]

# grammar repository 
grammar_repo = []

# read the input file, strip sentences
with open(input_file) as f:
    content = "".join(line.strip() for line in f if not line.isspace())

content = content.replace(iden,"").replace("("," ( ").replace(")"," ) ")
#print(content)

#s = "( TOP ( S ( NP ( DT The ) ( NNP Fulton ) ( NNP County ) ( NNP Grand ) ( NNP Jury ) ) ( VP ( VBD said ) ( NP ( NNP Friday ) ) ( SBAR ( -NONE- 0 ) ( S ( NP ( DT an ) ( NN investigation ) ( PP ( IN of ) ( NP ( NP ( NNP Atlanta ) ) ( POS 's ) ( JJ recent ) ( JJ primary ) ( NN election ) ) ) ) ( VP ( VBD produced ) ( NP ( `` `` ) ( DT no ) ( NN evidence ) ( '' '' ) ( SBAR ( IN that ) ( S ( NP ( DT any ) ( NNS irregularities ) )  ( VP ( VBD took ) ( NP ( NN place ) ) ) ) ) ) ) ) ) ) ) ( . . ) ) "

# clean the string (make sure there is no double space in it)
#s = s.replace("   ", " ").replace("  ", " ")
#print(s)
s = content.replace("   ", " ").replace("  ", " ")

# find inner parenthesis (no-need-to-parse-grammar) or (lhs rhs) format
simple_grammars = re.findall("\([^\(\)]*\)", s)
#print(simple_grammars)

clean_grammars = [g for g in simple_grammars if "NONE" not in g]
#print(clean_grammars)

# repeat until you cannot find any ( lhs rhs ) grammar
#while len(simple_grammars) > 0:    
while len(clean_grammars) > 0:
    # add all simple grammar into grammar repository
    # replace them with their head
    #for simple_grammar in simple_grammars:
    for simple_grammar in clean_grammars:
        #print(simple_grammar)
        grammar = simple_grammar.split(" ")
        # '(' == grammar[0] and ')' == grammar[-1]
        lhs = grammar[1]
        rhs = grammar[2:-1]
        if (lhs, rhs) not in grammar_repo:
            grammar_repo.append((lhs, rhs))
        
        s = s.replace(simple_grammar, lhs)

    simple_grammars = re.findall("\([^\(\)]*\)", s)
    #print(simple_grammars)
    clean_grammars = [g for g in simple_grammars if "NONE" not in g]
    #print(clean_grammars)

#print(grammar_repo)

# clean grammar repo
clean_grammar_repo = [g for g in grammar_repo if g[0] not in string.punctuation]
#print(clean_grammar_repo)

print(size(clean_grammar_repo))

final_grammar_set = []
for g in clean_grammar_repo:
    clean = True
    for rhs in g[1]:
        if rhs not in tagset:
            clean = False
    if clean:
        final_grammar_set.append(g)

#print(final_grammar_set)

print(size(final_grammar_set))

for g in final_grammar_set:
    t = g[0] + " ->"
    for ite in g[1]:
        t += " " + ite
    print(t)

# Distinct rules
print("Total distinct rules: ", len(final_grammar_set))

n_top = 10
# Counter frequency of rules
non_ter_list = [g[0] for g in final_grammar_set]
rule_count = Counter(non_ter_list)
#print(rule_count)
for rule, count in rule_count.most_common(n_top):
    print("{0}: {1}".format(rule, count))

print("The non-terminal with the most alternative rules: ", rule_count.most_common(1)[0][0])
