import datetime
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
    if punc:
        str += '.'
        spc = 0
        for i, char in enumerate(str):
            if char == ' ':
                spc += 1
                if spc == int(plen / 2):
                    str = str[:i] + ',' + str[i:]
    return str

def score_input(phrase, inpt):
    inpt = ' '.join(inpt.split())
    correct_ch = sum(list(map(lambda x, y: sum(x == y for x, y in zip(x, y)), phrase.split(), inpt.split())))
    return correct_ch / max(len(inpt.replace(' ', '')), 1), len(inpt) / 5 

def result_string(accuracy, wpm):
    return f'{round(100 * accuracy)}% | {round(accuracy * wpm)}wpm | {round(wpm)}raw'

def parse_args(args):
    caps, punc, clear, diff, plen = False, False, True, 10, 15
    for arg in args[1:]:
        if arg == '-caps': caps = True
        elif arg == '-punc': punc = True
        elif arg == '-noclear': clear = False
        elif re.search('^-diff=([1-9]|10)$', arg):
            diff = int(arg.strip('-diff='))
        elif re.search('^-len=([1-9]|[1-4][0-9]|50)$', arg):
            plen = int(arg.strip('-len='))
        else:
            raise ValueError('Illegal argument(s)!')
    diff = diff / 10 * len(words) - 1
    return caps, punc, clear, diff, plen

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    session_start = datetime.datetime.now().strftime('%m-%d-%Y %H.%M.%S')
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
            s = result_string(accuracy_avg, wpm_avg) + '\n'
            print('\n'.join(['[Session Average]'.center(len(s)), s]))
            with open(f'{os.path.dirname(__file__)}/results/{session_start}.txt', 'w+') as f:
                f.write('\n'.join(hist + ['[Session Average]'.center(len(s)), f'{s}\n']))
            exit()

