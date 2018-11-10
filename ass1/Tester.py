import sys

true_tag = sys.argv[1]
self_tag = sys.argv[2]

total_words_true_tag = 0
total_words_self_tag = 0
true_tag_list = []
self_tag_list = []

with open(true_tag, 'r') as true_tag:
    for line in true_tag:
        word_slash_tag = line.strip('\n').strip().split(" ")
        for t in word_slash_tag:
            total_words_true_tag += 1
            k = t.rfind("/")
            word, tag = t[:k], t[k + 1:]
            true_tag_list.append(tag)

with open(self_tag, 'r') as self_tag:
    for line in self_tag:
        word_slash_tag = line.strip('\n').strip().split(" ")
        for t in word_slash_tag:
            total_words_self_tag += 1
            k = t.rfind("/")
            word, tag = t[:k], t[k + 1:]
            self_tag_list.append(tag)

print("There are " + str(total_words_true_tag) + " words in TRUE tagged file")
print("There are " + str(total_words_self_tag) + " words in SELF tagged file")

total_true_tagged = 0
for true_tag, self_tag in zip(true_tag_list, self_tag_list):
    if true_tag == self_tag:
        total_true_tagged += 1


print("The file was tagged with: {:.2f} success percentage".format(100. *total_true_tagged / total_words_true_tag))
