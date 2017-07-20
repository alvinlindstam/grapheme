from unittest import TestCase

import grapheme
from grapheme import GraphemePropertyGroup


def test_has_legs():
    assert not grapheme.has_legs


class GetGroupTest(TestCase):
    def test_get_group_prepend(self):
        self.assertEqual(grapheme.get_group("\u0605"), GraphemePropertyGroup.PREPEND)

    def test_get_group_cr(self):
        self.assertEqual(grapheme.get_group("\u000D"), GraphemePropertyGroup.CR)

    def test_get_group_lf(self):
        self.assertEqual(grapheme.get_group("\u000A"), GraphemePropertyGroup.LF)

    def test_get_group(self):
        self.assertEqual(grapheme.get_group("s"), GraphemePropertyGroup.OTHER)
