import random
import time
import sys
import os

def import_words():
    words = []
    with open('words.txt', 'r') as f:
        words = [line.strip() for line in f.readlines()]
    return words

def generate_phrase(phrase_len, words, do_caps=True, do_punct=True):
    str = ''
    for i in range(phrase_len):
        str += words[random.randint(0, len(words) - 1)] + ' '
    str = str.strip()
    if do_caps:
        str = str.capitalize()
    if do_punct:
        str += '.'
    return str

def score_input(phrase, inpt):
    phrase = phrase.split()
    splinput = inpt.split()
    correct_w = 0
    for i, word in enumerate(phrase):
        try:
            if word == splinput[i]:
                correct_w += 1
        except:
            pass
    return correct_w / len(phrase), len(inpt) / 5

                
if __name__ == '__main__':
    os.system('clear')
    argv = sys.argv
    do_caps = '-capitals' in argv
    do_punct = '-punctuation' in argv
    words = import_words()
    phrase_len = 15
    wpm_avg = 0
    accuracy_avg = 0
    phrase_cnt = 0
    while True:
        try:
            phrase = generate_phrase(phrase_len, words, do_caps, do_punct)
            start_t = time.time()
            inpt = input('\n' + phrase + '\n').strip()
            elapsed_t = time.time() - start_t
            correct = score_input(phrase, inpt)
            wpm = 60 * correct[1] / elapsed_t
            accuracy = correct[0]
            phrase_cnt += 1
            wpm_avg = ((phrase_cnt - 1) * wpm_avg + wpm) / (phrase_cnt)
            accuracy_avg = ((phrase_cnt - 1) * accuracy_avg + accuracy) / (phrase_cnt)
            print(f'{round(100 * accuracy)}% | {round(accuracy * wpm)}wpm | {round(wpm)}raw')
        except KeyboardInterrupt:
            print(f'{round(100 * accuracy_avg)}% | {round(accuracy_avg * wpm_avg)}wpm | {round(wpm_avg)}raw')
            exit()

