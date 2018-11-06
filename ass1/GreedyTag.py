import sys
import MLETrain as mle

if len(sys.argv) < 6:
    print("Not enough arguments, quitting...")
    exit()
file_to_tag = sys.argv[1]
q_mle = sys.argv[2]
e_mle = sys.argv[3]
out_file = sys.argv[4]
extra_file = sys.argv[5]


def get_top_score_tag(x, t1, t2):
    top_score_tag = None
    max_score = 0
    for tag in mle.q_ones_c:
        q_score = mle.get_q(tag, t1, t2)
        e_score = mle.get_e(x, tag)
        temp_score = q_score + e_score
        if temp_score > max_score:
            max_score = temp_score
            top_score_tag = tag
    return top_score_tag


def greedy_tagger():
    output = open(out_file, 'w')
    with open(file_to_tag, 'r') as f:
        for line in f:
            word_tag = []
            prev1 = None
            prev2 = None
            words_in_line = line.strip('\n').strip().split(" ")
            for word in words_in_line:
                t = get_top_score_tag(word, prev2, prev1)
                if t is None:
                    t = "DT"
                word_tag.append((word, t))
                temp = prev1
                prev1 = t
                prev2 = temp
            write_list_as_line_to_open_file(output, word_tag)
    output.close()


def write_list_as_line_to_open_file(output_file, input_list):
    tagged_seq = ['/'.join(t) for t in input_list]
    final_seq = " ".join(tagged_seq) + "\n"
    output_file.write(final_seq)


if __name__ == '__main__':
    mle.init_counters(e_mle, q_mle)
    greedy_tagger()
