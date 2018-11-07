import sys
from collections import Counter

total_words_c = 0
e_mle_c = Counter()
q_triplet_c = Counter()
q_pairs_c = Counter()
q_ones_c = Counter()

lambda_1 = 0.5
lambda_2 = 0.3
lambda_3 = 0.2


def main():
    global e_mle_c, q_pairs_c, q_triplet_c, q_ones_c, total_words_c

    total_words_c = 0
    e_mle_c = Counter()
    q_triplet_c = Counter()
    q_pairs_c = Counter()
    q_ones_c = Counter()

    data = sys.argv[1]
    q_mle = sys.argv[2]
    e_mle = sys.argv[3]

    with open(data, 'r') as learn_data_file:
        for line in learn_data_file:
            prev1 = "STR"
            prev2 = "STR"
            word_slash_tag = line.strip('\n').strip().split(" ")
            for t in word_slash_tag:
                total_words_c += 1
                try:
                    k = t.rfind("/")
                    word, tag = t[:k], t[k + 1:]
                    e_mle_c[(word, tag)] += 1
                    q_ones_c[(tag,)] += 1
                    q_pairs_c[(prev1, tag)] += 1
                    q_triplet_c[(prev2, prev1, tag)] += 1
                    temp = prev1
                    prev1 = tag
                    prev2 = temp
                except Exception:
                    continue
    write_counter_to_file(e_mle_c, e_mle, 'w')
    write_counter_to_file(q_ones_c, q_mle, 'w')
    write_counter_to_file(q_pairs_c, q_mle, 'a')
    write_counter_to_file(q_triplet_c, q_mle, 'a')


def init_counters(e_mle_file, q_mle_file):
    global e_mle_c, q_pairs_c, q_triplet_c, q_ones_c, total_words_c

    total_words_c = 0
    e_mle_c = Counter()
    q_triplet_c = Counter()
    q_pairs_c = Counter()
    q_ones_c = Counter()

    with open(e_mle_file, 'r') as e_mle_learned_file:
        for line in e_mle_learned_file.readlines():
            line = line.strip("\n")
            if line == "":
                continue
            word_and_tag, value = line.split("\t")
            word, tag = word_and_tag.split(" ")
            value = int(value)
            total_words_c += value
            e_mle_c[(word, tag)] = value
    with open(q_mle_file, 'r') as q_mle_learned_file:
        for line in q_mle_learned_file.readlines():
            line = line.strip("\n")
            if line == "":
                continue
            tags, value = line.split("\t")
            value = int(value)
            tags_tuple = tuple(tags.split(" "))
            if len(tags_tuple) == 1:
                q_ones_c[tags_tuple] = value
            elif len(tags_tuple) == 2:
                q_pairs_c[tags_tuple] = value
            elif len(tags_tuple) == 3:
                q_triplet_c[tags_tuple] = value


def write_counter_to_file(counter, file_write, flag):
    with open(file_write, flag) as f:
        for t, val in counter.iteritems():
            tag = " ".join(t)
            f.write(tag + "\t" + str(val) + "\n")


def get_q(t1, t2, t3):
    """
    :param t1: a
    :param t2: b
    :param t3: c
    :return: probabilities
    """
    # deal with start in t2 and in t3
    denominator_t1_t2 = float(q_pairs_c[(t1, t2)])
    denominator_t_2 = float(q_ones_c[(t2,)])
    first_fraction = 0
    second_fraction = 0
    third_fraction = 0

    if denominator_t1_t2 > 0:
        first_fraction = float(q_triplet_c[(t1, t2, t3)]) / denominator_t1_t2
    if denominator_t_2 > 0:
        second_fraction = float(q_pairs_c[(t2, t3)]) / denominator_t_2
    if total_words_c > 0:
        third_fraction = float(q_ones_c[(t3,)]) / total_words_c
    return lambda_1 * first_fraction + lambda_2 * second_fraction + lambda_3 * third_fraction


def get_e(word, tag):
    if q_ones_c[(tag,)] ==0:
        print tag
        print q_ones_c[tag]
        print "cushilirabak"
        raw_input("enter bitch:!!!")
        return 0.3
    return float(e_mle_c[(word, tag)]) / q_ones_c[(tag,)]


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Not enough arguments, quitting...")
        exit()
    main()
