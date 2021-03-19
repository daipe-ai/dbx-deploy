import random
import string


class RandomStringGenerator:
    def generate(self, string_length: int):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(string_length))
