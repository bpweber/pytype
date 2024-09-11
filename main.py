import random
import time
import sys

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

if __name__ == '__main__':
    argv = sys.argv
    do_caps = '-capitals' in argv
    do_punct = '-punctuation' in argv
    words = import_words()
    phrase_len = 10
    wpm_avg = -1
    phrase_cnt = 0
    while True:
        phrase = generate_phrase(phrase_len, words, do_caps, do_punct)
        start_t = time.time()
        inpt = input('\n' + phrase + '\n').strip()
        elapsed_t = time.time() - start_t
        wpm = 60 * phrase_len // elapsed_t
        phrase_cnt += 1
        wpm_avg = ((phrase_cnt - 1) * wpm_avg + wpm) // (phrase_cnt)
        print(inpt == phrase, wpm, 'wpm', wpm_avg, 'avg')

