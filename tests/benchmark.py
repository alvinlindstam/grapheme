from random import choice
from string import ascii_lowercase
import timeit


def random_ascii_string(n):
    return "".join(choice(ascii_lowercase) for i in range(n))

long_ascii_string = random_ascii_string(10000)

statements = [
    ("len(long_ascii_string)", 1000),
    ("grapheme.length(long_ascii_string)", 500),
    ("grapheme.length(long_ascii_string, 500)", 1000),
    ("long_ascii_string[0:100]", 1000),
    ("grapheme.slice(long_ascii_string, 0, 100)", 1000),
    ("long_ascii_string[:100] in long_ascii_string", 1000),
    ("grapheme.contains(long_ascii_string, long_ascii_string[:100])", 500),
    ("long_ascii_string[-100:] in long_ascii_string", 1000),
    ("grapheme.contains(long_ascii_string, long_ascii_string[-100:])", 500),

]
for statement, n in statements:
    result = timeit.timeit(statement, setup="from __main__ import long_ascii_string; import grapheme", number=n) / 100
    print("{}: {} seconds".format(statement, result / n))

