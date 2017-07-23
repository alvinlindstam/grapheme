grapheme
========

A Python package for working with user perceived characters. More specifically,
string manipulation and calculation functions for workong with grapheme cluster
groups (graphemes) as defined by the `Unicode Standard Annex #29 <http://unicode.org/reports/tr29/>`__.

What? Why?
=========

Unicode strings are made up of a series of unicode characters, but a unicode character does not
always map to a user perceived character. Some human perceived characters are represented as two
or more unicode characters.

However, all built in python string functions and string methods work with single unicode characters
without considering their connection to each other.

.. code-block:: python

    >>> string = 'u̲n̲d̲e̲r̲l̲i̲n̲e̲d̲'
    >>> len(string)
    20
    >>> grapheme.length(string)
    10
    >>> string[:3]
    'u̲n'
    >>> grapheme.substr(string, 0, 3)
    'u̲n̲d̲'

This library implements the unicode default rules for extended grapheme clusters, and provides
a set of functions for string manipulation based on graphemes.

Documentation
====

todo: add docs

When should I consider graphemes instead of unicode characters?
====

You should consider working with graphemes over unicode code points when:

* You wish to count characters as perceived by users.
* You wish to split or truncate text at some user perceived lengths.
* You wish to split or truncate text without risk of corrupting the characters.
* Formatting text by length, such as creating text based tables in monospaced fonts

You should work with normal python string functions when:

* You wish to count or split by unicode codepoints for compliance with storage
  limitations (such as database maximum length)
* When working with systems that put limits on strings by unicode character
  lengths
* You absolutely require the performance benefits of using the built ins
* If simplicity is more important than accuracy

Performance
====

todo: make some benchmarks and work with performance fixes.

Examples of grapheme cluster groups
====

This is not a completet list, but a some examples of when graphemes use multiple
characters:

* CR+LF
* Hangul (korean)
* Emoji with modifiers
* Combining marks
* Zero Width Join

Development quick start
-------------------------

If you wish to contribute or edit this package, create a fork and clone it.

Then install in locally editable (``-e``) mode and run the tests.

.. code-block:: console

    pip install -e .[test]
    py.test
