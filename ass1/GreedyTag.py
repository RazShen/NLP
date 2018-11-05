import sys
from collections import Counter
import MLETrain as MLE

if len(sys.argv) < 6:
    print("Not enough arguments, quitting...")
    exit()

data = sys.argv[1]
q_mle = sys.argv[2]
e_mle = sys.argv[3]
out_file = sys.argv[4]
extra_file = sys.argv[5]

def get_top_score(x, t1, t2):
    max_score = 0
    max_t = 0
    # if (t1 == None and t2 == None)
    for tag in MLE.q_ones_c:
        q_score = MLE.getQ(tag, t1, t2)
        e_score = MLE.getE(x, tag)
        temp_score = q_score * e_score
        if temp_score > max_score:
            max_score = temp_score
    return max_score

def greedy_tagger():
    with open(data,'r') as d:
        for line in d:
            prev1 = None
            prev2 = None
            line = line.replace('\n', "")
            word_slash = line.strip('\n').strip().split(" ")
            for word in word_slash:
                try:
                    t = get_top_score(word, prev1, prev2)
                    temp = prev1
                    prev1 = t
                    prev2 = temp
                except Exception:
                    continue