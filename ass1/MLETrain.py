import sys

# Checking valid input
if len(sys.argv) < 4:
    print("Not enough arguments, quitting...")
    exit()

data = sys.argv[1]
q_mle = sys.argv[2]
e_mle = sys.argv[3]
e_mle_d = {}

def write_e_dict_to_file(dictionary, dict_file_name):
    with open(dict_file_name, 'w') as file:
        for t in dictionary:
            word, tag = t
            file.write(word + " " + tag + "\t" + str(dictionary[t]) + '\n')


def add_to_dict(dictionary, word):
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1

with open(data,'r') as d:
    for line in d:
        line = line.replace('\n', "")
        word_slash = line.strip('\n').strip().split(" ")
        for t in word_slash:
            try:
                k = t.rfind("/")
                word, tag = t[:k], t[k+1:]
                add_to_dict(e_mle_d, (word,tag))
            except Exception:
                continue

write_e_dict_to_file(e_mle_d, e_mle)