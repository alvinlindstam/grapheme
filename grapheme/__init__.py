"""
Main module for the grapheme package.

.. data:: UNICODE_VERSION

    The currently supported Unicode version
"""

from .api import (graphemes, length, grapheme_lengths, slice, contains, safe_split_index, startswith, endswith,
                  UNICODE_VERSION)

__all__ = ['graphemes', 'length', 'grapheme_lengths', 'slice', 'contains', 'safe_split_index', 'startswith', 'endswith',
           'UNICODE_VERSION']
