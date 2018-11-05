import sys
from collections import Counter

# Checking valid input
if len(sys.argv) < 4:
    print("Not enough arguments, quitting...")
    exit()

data = sys.argv[1]
q_mle = sys.argv[2]
e_mle = sys.argv[3]
e_mle_c = Counter()
q_triplet_c = Counter()
q_pairs_c = Counter()
q_ones_c = Counter()
total_words_c = 0
c1 = 0.5
c2 = 0.3
c3 = 0.2
def write_counter_to_file(counter, file_write,flag):
    with open(file_write, flag) as f:
        for t, val in counter.iteritems():
            tag = " ".join(t)
            f.write(tag + "\t" + str(val) + "\n")

def getQ(t1,t2,t3):
    #todo: deal
    return 5
    if (q_pairs_c[(t1,t2)] == 0):
        return c2 * (q_pairs_c[(t2,t3)]/q_ones_c[(t2,)]) + c3 * (q_ones_c[(t1,)/total_words_c])
    elif (q_ones_c[(t2)]):
        return 5
    return c1 * (q_triplet_c[(t1,t2,t3)]/q_pairs_c[(t1,t2)]) + c2 * (q_pairs_c[(t2,t3)]/q_ones_c[(t2,)]) + c3 * (q_ones_c[(t1,)/total_words_c])

def getE(word,tag):
    return 5
    if (q_ones_c[(tag,)] == 0):
        return 100000
    else:
        return (e_mle_c[(word,tag)] / q_ones_c[(tag,)])
with open(data,'r') as d:
    for line in d:
        prev1 = None
        prev2 = None
        line = line.replace('\n', "")
        word_slash = line.strip('\n').strip().split(" ")
        for t in word_slash:
            total_words_c += 1
            try:
                k = t.rfind("/")
                word, tag = t[:k], t[k+1:]
                e_mle_c[(word,tag)] += 1
                q_ones_c[(tag,)] += 1
                if prev1 != None:
                    q_pairs_c[(prev1, tag)] += 1
                if prev2 != None:
                    q_triplet_c[(prev2, prev1, tag)] += 1
                temp = prev1
                prev1 = tag
                prev2 = temp
            except Exception:
                continue



write_counter_to_file(e_mle_c,e_mle, 'w')
write_counter_to_file(q_ones_c,q_mle, 'w')
write_counter_to_file(q_pairs_c,q_mle, 'a')
write_counter_to_file(q_triplet_c,q_mle, 'a')