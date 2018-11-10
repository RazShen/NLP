import sys
import MLETrain as mle

if len(sys.argv) < 6:
    print("Not enough arguments, quitting...")
    exit()

file_to_tag = sys.argv[1]
q_mle_file = sys.argv[2]
e_mle_file = sys.argv[3]
out_file = sys.argv[4]
extra_file = sys.argv[5]


def get_top_score_tag(x, t1, t2):
    top_score_tag = mle.q_ones_c.keys()[0][0]
    max_score = 0
    seen_word = False
    for tag_tuple in mle.q_ones_c:
        t = tag_tuple[0]
        if mle.get_e(x, t) > 0:
            seen_word = True
            break
    if not seen_word:
        e_score_tag = mle.get_e_score_for_unseen(x)  # e_score here is tag
        e_score = mle.get_q(t2, t1, e_score_tag)
    for tag_tuple in mle.q_ones_c:
        t = tag_tuple[0]
        q_score = mle.get_q(t2, t1, t)  # t2 (y_i-2) = a, t1(y_i-1) = b, tag =c
        if seen_word:
            e_score = mle.get_e(x, t)
        temp_score = q_score * e_score
        if temp_score > max_score:
            max_score = temp_score
            top_score_tag = t
    return top_score_tag


def greedy_tagger():
    output = open(out_file, 'w')
    with open(file_to_tag, 'r') as f:
        for line in f:
            word_tag = []
            prev1 = "STR"
            prev2 = "STR"
            words_in_line = line.strip('\n').strip().split(" ")
            for word in words_in_line:
                t = get_top_score_tag(word, prev1, prev2)
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
    mle.init_counters(e_mle_file, q_mle_file)
    mle.init_signature_tags_dicts(e_mle_file)
    greedy_tagger()
