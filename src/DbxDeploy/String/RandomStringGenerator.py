import random
import string

class RandomStringGenerator:

    def generate(self, stringLength: int):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
