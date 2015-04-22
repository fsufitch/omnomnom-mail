import random

class WeightedDictionary(object):
    def __init__(self):
        # [(start_int, end_int, choice), ...]
        self.choices = []

        self.start_weight = 0
        self.end_weight = 0

    def add_choice(self, choice, weight):
        new_choice = self.end_weight, self.end_weight + weight, choice
        self.end_weight += weight
        self.choices.append(new_choice)

    def choose(self):
        assert self.end_weight > 0
        choice_number = random.uniform(self.start_weight, self.end_weight)
        choice = self._find(choice_number, 0, len(self.choices))
        return choice
        
    def _find(self, choice_weight, start, end):
        # Binary search!
        current = (start + end) // 2
        weight1, weight2, choice_str = self.choices[current]

        if end-start<1:
            return None
        if weight1 < choice_weight < weight2:
            return choice_str # Found!
        if choice_weight < weight1:
            return self._find(choice_weight, start, current)
        if choice_weight > weight2:
            return self._find(choice_weight, current, end)
        raise SystemError("The universe broke, you shouldn't be here.")
