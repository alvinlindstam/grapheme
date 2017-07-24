
from grapheme.finder import GraphemeIterator

def graphemes(string):
    """
    Returns an iterator of all graphemes of given string.

    >>> rainbow_flag = "🏳️‍🌈"
    >>> []
    >>> [codepoint for codepoint in rainbow_flag]
    ['🏳', '️', '\u200d', '🌈']
    >>> list(grapheme.graphemes("multi codepoint grapheme: " + rainbow_flag))
    ['m', 'u', 'l', 't', 'i', ' ', 'c', 'o', 'd', 'e', 'p', 'o', 'i', 'n', 't', ' ', 'g', 'r', 'a', 'p', 'h', 'e', 'm', 'e', ':', ' ', '🏳️‍🌈']
    """
    return iter(GraphemeIterator(string))


def length(string, until=None):
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


def substr(string, start, end):
    if start >= end:
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
