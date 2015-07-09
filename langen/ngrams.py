import random

def get_grams(corpus, size=3):
    """Returns a grams dict, of the form {'key1 key2 ...': [choice1, choice2, ...], ...}
    
    :param corpus: a list (or iterator) of words.
    
    :param size: the size of each n-gram"""
    if size < 2:
        e = ValueError('size must be at least 2')
        raise e
    corpus = list(corpus)
    grams = {}
    while len(corpus) >= size:
        key = ' '.join([corpus.pop(0)] + corpus[:size - 2])
        grams.setdefault(key, []).append(corpus[size - 2])
    return grams

def gram_generator(grams, maxlen=100, choicefunc=random.choice, case_sensitive=True, seed=None):
    """Return a generator that yields each next word based on a grams dict
    
    :param grams: A dict of n-grams, probably from get_grams().
    
    :param maxlength: if 0, the generator will only stop if the next key cannot be found.
    
    :param choicefunc: a function that returns one element from a list. Only
        replace if you want a special distribution, or for debugging purposes.
    
    :param case_sensitive: True if a keys should not be matched if they have a different case.
                           False if case variants can count.
    
    :param seed: A starting key, defaults to a random choice (dictated by choicefunc) of
        of the keys in grams"""
    curlen = 0
    key = choicefunc(tuple(grams.keys())) if seed is None else seed
    for word in key.split():
        if curlen > maxlen:
            return
        curlen += 1
        yield word
    key = key if case_sensitive else key.lower()
    while maxlen == 0 or curlen <= maxlen:
        if key not in grams:
            return
        next_word = choicefunc(grams[key])
        key = ' '.join(key.split()[1:]) + ' ' + next_word
        key = key if case_sensitive else key.lower()
        curlen += 1
        yield next_word

def demo():
    with open('samples/ngrams_corpus.txt') as f:
        corpus = f.read().replace('--', ' ').replace(',', ' ').split()
    grams = get_grams(corpus, size=3)
    for word in gram_generator(grams, maxlength=200):
        print(word, end=' ')

if __name__ == '__main__':
    demo()
