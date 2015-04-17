import random
from pkg_resources import resource_filename

class NameGenerator(object):
    # word list sourced from https://github.com/kevina/wordlist/tree/master/pos
    def __init__(self):
        self.words = {}
        
    def reload(self, fobj):
        new_words = {}
        for line in fobj:
            line = line.strip()
            word, parts_of_speech = line.split("\t")
            if not word.isalpha():
                continue # Look only for simple words
            word = word.lower()
            for pos in parts_of_speech:
                if pos not in new_words:
                    new_words[pos] = []
                new_words[pos].append(word)
        self.words = new_words

    def random_noun(self):
        nouns = self.words.get('N', [])
        plurals = self.words.get('P', [])
        return random.choice(nouns+plurals)

    def random_adjective(self):
        adjectives = self.words.get('A', [])
        return random.choice(adjectives)

    _INSTANCE = None
    @classmethod
    def instance(cls, wordpath=None, force=False):
        if cls._INSTANCE and wordpath and not force:
            raise Exception("Reloading generator not permitted (use force=True to force it)")

        if not cls._INSTANCE:
            if not wordpath:
                # Needs initialization, but no path given; get default path
                wordpath = resource_filename(__name__, 'part-of-speech.txt')
            cls._INSTANCE = NameGenerator()
            with open(wordpath) as f:
                cls._INSTANCE.reload(f)
        elif wordpath and force:
            # Load/reload
            with open(wordpath) as f:
                cls._INSTANCE.reload(open(wordpath))
        return cls._INSTANCE
            
