"""
A library for working with grapheme cluster groups (graphemes), as defined by
the Unicode Standard.

A grapheme is single character, as perceived by users. Some graphemes are
represented as multiple unicode characters (code points), yet still be
connected visually and semantically.

Pythons built in string functions work with unicode code points as the basic
unit, so lengths, slicing, matching etc is done on the code points. This
module adds helper functions for common string operations with respect to
graphemes instead.
"""
from .grapheme_property_group import get_group, GraphemePropertyGroup

from .api import graphemes, length, grapheme_lengths, slice

__all__ = ['graphemes', 'length', 'grapheme_lengths', 'slice']
