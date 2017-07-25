.. grapheme documentation master file, created by
   sphinx-quickstart on Mon Jul 24 23:09:29 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

grapheme
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   grapheme

A library for working with grapheme cluster groups (graphemes), as defined by
the Unicode Standard.

A grapheme is single character, as perceived by users. Some graphemes are
represented as multiple unicode characters (code points), yet still be
connected visually and semantically.

Pythons built in string functions work with unicode code points as the basic
unit, so lengths, slicing, matching etc is done on the code points. This
module adds helper functions for common string operations with respect to
graphemes instead.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
