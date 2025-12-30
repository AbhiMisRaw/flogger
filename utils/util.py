import random
import string

class Util:

    @staticmethod
    def random_code(length=6):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))