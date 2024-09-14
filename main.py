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
    if caps: str = str[0].upper() + str[1:]
    if punc: str += '.'
    return str

def score_input(phrase, inpt):
    inpt = ' '.join(inpt.split())
    correct_ch = sum(list(map(lambda x, y: sum(x == y for x, y in zip(x, y)), phrase.split(), inpt.split())))
    return correct_ch / len(inpt.replace(' ', '')), len(inpt) / 5 

def result_string(accuracy, wpm):
    return f'{round(100 * accuracy)}% | {round(accuracy * wpm)}wpm | {round(wpm)}raw'

def parse_args(args):
    caps, punc, clear = '-caps' in args, '-punc' in args, '-noclear' not in args
    diff = re.search('-diff=[0-9]+', ' '.join(args))
    diff = min(int(diff.group().strip('-diff=')) if diff else 10, 10)
    diff = max(int(diff / 10 * len(words) - 1), 1)
    plen = re.search('-len=[0-9]+', ' '.join(args))
    plen = min(int(plen.group().strip('-len=')) if plen else 15, 50)
    return caps, punc, clear, diff, plen

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    words = import_words()
    caps, punc, clear, diff, plen = parse_args(sys.argv)
    wpm_avg = 0
    accuracy_avg = 0
    ctr = 0
    hist = []
    while True:
        try:
            if clear: os.system('cls' if os.name == 'nt' else 'clear')
            phrase = generate_phrase(words, plen, diff, caps, punc)
            start_t = time.time()
            inpt = input(f'{phrase} ⏎\n').strip()
            elapsed_t = time.time() - start_t
            accuracy, correct = score_input(phrase, inpt)
            wpm = 60 * correct / elapsed_t
            wpm_avg = (ctr * wpm_avg + wpm) / (ctr + 1)
            accuracy_avg = (ctr * accuracy_avg + accuracy) / (ctr + 1)
            s = result_string(accuracy, wpm) + '\n' 
            hist.extend([f'{phrase} ⏎', inpt, s])
            print(s)
            ctr += 1
        except KeyboardInterrupt:
            sys.stdout.write('\033[F\033[K')
            if clear: print('\n'.join(hist))
            s = result_string(accuracy_avg, wpm_avg)
            print('[Session Average]'.center(len(s)))
            print(s)
            exit()

