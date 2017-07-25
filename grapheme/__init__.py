"""
Main module for the grapheme package.
"""

from .grapheme_property_group import get_group, GraphemePropertyGroup

from .api import graphemes, length, grapheme_lengths, slice

__all__ = ['graphemes', 'length', 'grapheme_lengths', 'slice']
