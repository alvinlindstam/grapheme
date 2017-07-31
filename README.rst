grapheme
========

A Python package for working with user perceived characters. More specifically,
string manipulation and calculation functions for workong with grapheme cluster
groups (graphemes) as defined by the `Unicode Standard Annex #29 <http://unicode.org/reports/tr29/>`_.

`documentation <https://grapheme.readthedocs.io/>`_

.. code-block:: console

    pip install grapheme

What? Why?
==========

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
=============

See `<https://grapheme.readthedocs.io/en/latest/>`_.

When should I consider graphemes instead of unicode characters?
===============================================================

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
* When you prioritize performance over correctness (see performance notes below)
* When working with very long strings (see performance notes below)
* If simplicity is more important than accuracy

Performance
===========

Calculating graphemes require traversing the string and checking each character
against a set of rules and the previous character(s). Because of this, all
functions in this module will scale linearly to the string length.

Whenever possible, they will only traverse the string for as long as needed and return
early as soon as the requested output is generated. For example, the `grapheme.slice`
function only has to traverse the string until the last requested grapheme is found, and
does not care about the rest of the string.

You should probably only use this package for testing/manipulating fairly short strings
or with the beginning of long strings.

When testing with a string of 10 000 ascii characters, and a 3.1 GHz processor, the execution
time is for some possible calls is roughly:

================================================================  ==========================
Code                                                              Approximate execution time
================================================================  ==========================
`len(long_ascii_string)`                                          8.1e-10 seconds
`grapheme.length(long_ascii_string)`                              1.5e-04 seconds
`grapheme.length(long_ascii_string, 500)`                         8.7e-06 seconds
`long_ascii_string[0:100]`                                        1.3e-09 seconds
`grapheme.slice(long_ascii_string, 0, 100)`                       2.5e-06 seconds
`long_ascii_string[:100] in long_ascii_string`                    4.0e-09 seconds
`grapheme.contains(long_ascii_string, long_ascii_string[:100])`   3.9e-06 seconds
`long_ascii_string[-100:] in long_ascii_string`                   2.1e-07 seconds
`grapheme.contains(long_ascii_string, long_ascii_string[-100:])`  1.9e-04 seconds
================================================================  ==========================

Execution times may improve in later releases, but calculating graphemes is and will continue
to be notably slower than just counting unicode code points.

Examples of grapheme cluster groups
===================================

This is not a complete list, but a some examples of when graphemes use multiple
characters:

* CR+LF
* Hangul (korean)
* Emoji with modifiers
* Combining marks
* Zero Width Join

Development quick start
=======================

If you wish to contribute or edit this package, create a fork and clone it.

Then install in locally editable (``-e``) mode and run the tests.

.. code-block:: console

    pip install -e .[test]
    py.test
