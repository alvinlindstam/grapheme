## 0.4.0
Added support for Unicode 11.

Added `grapheme.UNICODE_VERSION`.

No other API changes

## 0.3.0
Added a few new functions:

* `grapheme.safe_split_index`, which can find the highest grapheme boundary index in a given string without traversing the full grapheme sequence.
* `grapheme.startswith`, which tests that a given string starts with the same grapheme sequence as a given prefix.
* `grapheme.endswith`, which tests that a given string ends with the same grapheme sequence as a given suffix.

## 0.2.1
Performance improvements

No new functionality, but noticably better performance.

## 0.2.0
* Adds `grapheme.contains`
* Bugfix for empty strings

## 0.1.0
Initial release

Basic support for getting graphemes, grapheme string lengths and grapheme based slicing.
