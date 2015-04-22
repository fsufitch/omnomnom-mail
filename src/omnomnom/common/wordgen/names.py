import random
from pkg_resources import resource_filename

from omnomnom.common.wordgen.dictionary import WeightedDictionary

class NameDB(object):
    def __init__(self, fileobj):
        self.name_chooser = WeightedDictionary()
        for line in fileobj:
            name, weight, *other = line.split()
            name = name.title()
            weight = float(weight)
            if not weight:
                continue
            self.name_chooser.add_choice(name, weight)

    def get_name(self):
        return self.name_chooser.choose()

class FullNameGenerator(object):
    LAST_PATH = resource_filename(__name__, 'dist.all.last')
    FIRST_MALE_PATH = resource_filename(__name__, 'dist.male.first')
    FIRST_FEMALE_PATH = resource_filename(__name__, 'dist.female.first')
    def __init__(self):
        with open(self.LAST_PATH) as f:
            self.last_names = NameDB(f)
        with open(self.FIRST_MALE_PATH) as f:
            self.first_male_names = NameDB(f)
        with open(self.FIRST_FEMALE_PATH) as f:
            self.first_female_names = NameDB(f)
            
    def get_name(self):
        is_male = random.uniform(0, 1) < 0.5

        first = self.first_male_names.get_name() if is_male else self.first_female_names.get_name()
        last = self.last_names.get_name()
        mi = None
        if random.uniform(0,1) < 0.7:
            mi = chr(random.randint(65, 65+25))

        return first, mi, last

    _INSTANCE = None
    @classmethod
    def instance(cls):
        if not cls._INSTANCE:
            cls._INSTANCE = cls()
        return cls._INSTANCE
