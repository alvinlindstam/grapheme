
from grapheme.finder import GraphemeIterator

def graphemes(string):
    """
    Returns an iterator of all graphemes of given string.

    >>> rainbow_flag = "🏳️‍🌈"
    >>> [codepoint for codepoint in rainbow_flag]
    ['🏳', '️', '\u200d', '🌈']
    >>> list(grapheme.graphemes("multi codepoint grapheme: " + rainbow_flag))
    ['m', 'u', 'l', 't', 'i', ' ', 'c', 'o', 'd', 'e', 'p', 'o', 'i', 'n', 't', ' ', 'g', 'r', 'a', 'p', 'h', 'e', 'm', 'e', ':', ' ', '🏳️‍🌈']
    """
    return iter(GraphemeIterator(string))


def length(string, until=None):
    """
    Returns the number of graphemes in the string.

    Note that this functions needs to traverse the full string to calculate the length,
    unlike `len(string)`.

    Only counts up to the `until` argument, if given. This is useful when testing
    the length of a string against some limit and the excess length is not interesting.

    >>> rainbow_flag = "🏳️‍🌈"
    >>> len(rainbow_flag)
    4
    >>> graphemes.length(rainbow_flag)
    1
    >>> graphemes.length("".join(str(i) for i in range(100)), 30)
    30
    """
    if until is None:
        return sum(1 for _ in GraphemeIterator(string))

    iterator = graphemes(string)
    count = 0
    while True:
        try:
            if count >= until:
                break
            next(iterator)
        except StopIteration:
            break
        else:
            count += 1

    return count


# todo: should probably use an optimized iterator that only deals with code point counts (optimization)
def grapheme_lengths(string):
    return (len(g) for g in graphemes(string))


def slice(string, start=None, end=None):
    """
    Returns a substring of the given string, counting graphemes instead of codepoints.

    Negative indices is not supported.

    >>> string = "tamil நி (ni)"
    >>> string[:7]
    'tamil ந'
    >>> grapheme.slice(string, end=7)
    'tamil நி'
    >>> string[7:]
    'ி (ni)'
    >>> grapheme.slice(string, 7)
    ' (ni)'
    """

    if start is None:
        start = 0
    if end is not None and start >= end:
        return ""

    if start < 0:
        raise NotImplementedError("Negative indexing is currently not supported.")

    sum_ = 0
    start_index = None
    for grapheme_index, grapheme_length in enumerate(grapheme_lengths(string)):
        if grapheme_index == start:
            start_index = sum_
        elif grapheme_index == end:
            return string[start_index:sum_]
        sum_ += grapheme_length

    if start_index is not None:
        return string[start_index:]

    return ""
