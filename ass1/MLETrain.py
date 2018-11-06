import sys
from collections import Counter
import random
# Checking valid input

total_words_c = 0
e_mle_c = Counter()
q_triplet_c = Counter()
q_pairs_c = Counter()
q_ones_c = Counter()

c1 = 0.5
c2 = 0.3
c3 = 0.2

def main():
    global total_words_c
    total_words_c = 0
    global e_mle_c
    e_mle_c = Counter()

    global q_triplet_c
    q_triplet_c = Counter()

    global q_pairs_c
    q_pairs_c = Counter()

    global q_ones_c
    q_ones_c = Counter()

    data = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3] 
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


def init_counters(e_mle_file, q_mle_file):
    global e_mle_c
    e_mle_c = Counter()

    global q_triplet_c
    q_triplet_c = Counter()

    global q_pairs_c
    q_pairs_c = Counter()

    global q_ones_c
    q_ones_c = Counter()

    with open(e_mle_file, 'r') as f:
        content = f.readlines()
        for line in content:
            line = line.strip("\n")
            if line == "":
                continue
            key, value = line.split("\t")
            word,tag = key.split(" ")
            value = int(value)
            e_mle_c[(word,tag)] = value
    with open(q_mle_file, 'r') as f:
        content = f.readlines()
        for line in content:
            line = line.strip("\n")
            if line == "":
                continue
            key, value = line.split("\t")
            value = int(value)
            tags = tuple(key.split(" "))
            if (len(tags) ==1):
                q_ones_c[tags] = value
            elif (len(tags)==2):
                q_pairs_c[tags] = value
            elif (len(tags) == 3):
                q_triplet_c[tags] = value

def write_counter_to_file(counter, file_write,flag):
    with open(file_write, flag) as f:
        for t, val in counter.iteritems():
            tag = " ".join(t)
            f.write(tag + "\t" + str(val) + "\n")

def getQ(t1,t2,t3):
    #todo: deal with start in t1 and in t2
    return random.uniform(0, 1)
    divided_pairs = q_pairs_c[(t1,t2)]
    divided_ones = q_ones_c[(t2,)]
    if (q_pairs_c[(t1,t2)] == 0):
        divided_pairs = 1
    if (q_ones_c[(t2,)]):
        divided_ones = 1
    return c1 * (q_triplet_c[(t1,t2,t3)]/ divided_pairs) + c2 * (q_pairs_c[(t2,t3)]/divided_ones) + c3 * (q_ones_c[(t1,)]/total_words_c)

def getE(word,tag):
    return random.uniform(0, 1)
    if (q_ones_c[(tag,)] == 0):
        return 0.01
    else:
        return (e_mle_c[(word,tag)] / q_ones_c[(tag,)])

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Not enough arguments, quitting...")
        exit()
    main()





