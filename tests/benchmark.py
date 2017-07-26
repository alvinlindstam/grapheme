from random import choice
from string import ascii_lowercase
import timeit

import grapheme

def random_ascii_string(n):
    return "".join(choice(ascii_lowercase) for i in range(n))

long_ascii_string = random_ascii_string(1000)

statements = [
    "len(long_ascii_string)",
    "grapheme.length(long_ascii_string)",
]
for statement in statements:
    n = 100
    result = timeit.timeit(statement, setup="from __main__ import long_ascii_string; import grapheme", number=n) / 100
    print("{}: {} seconds".format(statement, result))

