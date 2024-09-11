import random
import time
def import_words():
    words = []
    with open('words.txt', 'r') as f:
        words = [line.strip() for line in f.readlines()]
    return words

def generate_phrase(phrase_len, words):
    str = ''
    for i in range(phrase_len):
        str += words[random.randint(0, len(words))] + ' '
    return str.strip()

if __name__ == '__main__':
#   print(import_words())
    words = import_words()
    phrase_len = 10
    while True:
        phrase = generate_phrase(phrase_len, words)
        start_t = time.time()
        inpt = input('\n' + phrase + '\n').strip()
        elapsed_t = time.time() - start_t
        wpm = 60 * phrase_len // elapsed_t
        print(inpt == phrase, wpm, 'wpm')
