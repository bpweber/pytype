import random
import time
import sys
import os
import re

def import_words():
    with open('words.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

def generate_phrase(words, plen, diff, caps, punc):
    str = ' '.join([words[random.randint(0, diff)] for _ in range(plen)])
    if caps:
        str = str.capitalize()
    if punc:
        str += '.'
    return str

def score_input(phrase, inpt):
    correct_ch = sum(list(map(lambda x, y: sum(x == y for x, y in zip(x, y)), phrase.split(), inpt.split())))
    return correct_ch / len(phrase.replace(' ', '')), len(inpt) / 5

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    words = import_words()
    caps, punc = '-caps' in sys.argv, '-punc' in sys.argv
    diff = re.search('-diff=[0-9]+', ' '.join(sys.argv))
    diff = min(int(diff.group().strip('-diff=')) if diff else len(words) - 1, len(words) - 1)
    plen = re.search('-len=[0-9]+', ' '.join(sys.argv))
    plen = min(int(plen.group().strip('-len=')) if plen else 15, 250)
    print(diff, plen)
    wpm_avg = 0
    accuracy_avg = 0
    ctr = 0
    while True:
        try:
            phrase = generate_phrase(words, plen, diff, caps, punc)
            start_t = time.time()
            inpt = input('\n' + phrase + '\n').strip()
            elapsed_t = time.time() - start_t
            accuracy, correct = score_input(phrase, inpt)
            wpm = 60 * correct / elapsed_t
            wpm_avg = (ctr * wpm_avg + wpm) / (ctr + 1)
            accuracy_avg = (ctr * accuracy_avg + accuracy) / (ctr + 1)
            ctr += 1
            print(f'{round(100 * accuracy)}% | {round(accuracy * wpm)}wpm | {round(wpm)}raw')
        except KeyboardInterrupt:
            print(f'{round(100 * accuracy_avg)}% | {round(accuracy_avg * wpm_avg)}wpm | {round(wpm_avg)}raw')
            exit()

