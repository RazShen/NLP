import sys
import MLETrain as mle

if len(sys.argv) < 6:
    print("Not enough arguments, quitting...")
    exit()
data = sys.argv[1]
q_mle = sys.argv[2]
e_mle = sys.argv[3]
out_file = sys.argv[4]
extra_file = sys.argv[5]


def get_top_score(x, t1, t2):
    top_tag = None
    max_score = 0
    for tag in mle.q_ones_c:
        tag = tag[0]
        q_score = mle.getQ(tag, t1, t2)
        e_score = mle.getE(x, tag)
        temp_score = q_score + e_score
        if temp_score > max_score:
            max_score = temp_score
            top_tag = tag
    return top_tag


def greedy_tagger():
    output = open(out_file, 'w')
    with open(data, 'r') as d:
        for line in d:
            word_tag = []
            prev1 = None
            prev2 = None
            line = line.replace('\n', "")
            word_slash = line.strip('\n').strip().split(" ")
            for word in word_slash:
                t = get_top_score(word, prev1, prev2)
                word_tag.append((word, t))
                temp = prev1
                prev1 = t
                prev2 = temp
            write_list_as_line_to_open_file(output, word_tag)
    output.close()


def write_list_as_line_to_open_file(output_file, input_list):
    tagged_seq = ['/'.join(tupl) for tupl in input_list]
    final_seq = " ".join(tagged_seq) + "\n"
    output_file.write(final_seq)


if __name__ == '__main__':
    mle.init_counters(e_mle, q_mle)
    greedy_tagger()
