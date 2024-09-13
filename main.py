import random
import time
import sys
import os

def import_words():
    with open('words.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

def generate_phrase(phrase_len, words, do_caps=True, do_punct=True):
    str = ' '.join([words[random.randint(0, len(words) - 1)] for _ in range(phrase_len)])
    if do_caps:
        str = str.capitalize()
    if do_punct:
        str += '.'
    return str

def score_input(phrase, inpt):
    correct_ch = sum(list(map(lambda x, y: sum(x == y for x, y in zip(x, y)), phrase.split(), inpt.split())))
    return correct_ch / len(phrase.replace(' ', '')), len(inpt) / 5

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    argv = sys.argv
    do_caps = '-caps' in argv
    do_punct = '-punc' in argv
    words = import_words()
    phrase_len = 15
    wpm_avg = 0
    accuracy_avg = 0
    ctr = 0
    while True:
        try:
            phrase = generate_phrase(phrase_len, words, do_caps, do_punct)
            start_t = time.time()
            inpt = input('\n' + phrase + '\n').strip()
            elapsed_t = time.time() - start_t
            accuracy, correct = score_input(phrase, inpt)
            wpm = 60 * correct / elapsed_t
            ctr += 1
            wpm_avg = ((ctr - 1) * wpm_avg + wpm) / (ctr)
            accuracy_avg = ((ctr - 1) * accuracy_avg + accuracy) / (ctr)
            print(f'{round(100 * accuracy)}% | {round(accuracy * wpm)}wpm | {round(wpm)}raw')
        except KeyboardInterrupt:
            print(f'{round(100 * accuracy_avg)}% | {round(accuracy_avg * wpm_avg)}wpm | {round(wpm_avg)}raw')
            exit()

