import random
import string


def get_unique_short_id(original_link, short_path=None):
    symbols = string.digits + string.ascii_letters
    short_id = random.choice(symbols)
    short_id= ''.join(random.choice(symbols) for i in range(6))
    return short_id

print(get_unique_short_id('https://yandex.ru'))
