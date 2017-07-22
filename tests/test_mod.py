#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from unittest import TestCase

import pytest

from grapheme.grapheme_property_group import GraphemePropertyGroup, get_group
import grapheme

class GetGroupTest(TestCase):
    def test_get_group_prepend(self):
        self.assertEqual(get_group("\u0605"), GraphemePropertyGroup.PREPEND)

    def test_get_group_cr(self):
        self.assertEqual(get_group("\u000D"), GraphemePropertyGroup.CR)

    def test_get_group_lf(self):
        self.assertEqual(get_group("\u000A"), GraphemePropertyGroup.LF)

    def test_get_group(self):
        self.assertEqual(get_group("s"), GraphemePropertyGroup.OTHER)

class GraphemesTest(TestCase):
    def test_simple(self):
        self.assertEqual(list(grapheme.graphemes("alvin")), list("alvin"))

    def test_emoji_with_modifier(self):
        input_str = "\U0001F476\U0001F3FB"
        self.assertEqual(list(grapheme.graphemes(input_str)), [input_str])

    def test_cr_lf(self):
        self.assertEqual(list(grapheme.graphemes("\u000D\u000A")), ["\u000D\u000A"])

    def test_mixed_text(self):
        input_str = " \U0001F476\U0001F3FB ascii \u000D\u000A"
        graphemes = [" ", "\U0001F476\U0001F3FB", " ",  "a", "s", "c", "i", "i", " ", input_str[-2:]]
        self.assertEqual(list(grapheme.graphemes(input_str)), graphemes)
        self.assertEqual(list(grapheme.grapheme_lengths(input_str)), [len(g) for g in graphemes])
        self.assertEqual(grapheme.substr(input_str, 0, 2), " \U0001F476\U0001F3FB")
        self.assertEqual(grapheme.substr(input_str, 0, 3), " \U0001F476\U0001F3FB ")
        self.assertEqual(grapheme.substr(input_str, 1, 4), "\U0001F476\U0001F3FB a")
        self.assertEqual(grapheme.substr(input_str, 2, 4), " a")

TEST_CASES = []

with open(os.path.join(os.path.dirname(__file__), "../unicode-data/GraphemeBreakTest.txt"), 'r') as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue

        test_data, description = line.split("#")

        expected_graphemes = [
            "".join([
                chr(int(char, 16)) for char in cluster.split("×") if char.strip()
            ])
            for cluster in test_data.split("÷") if cluster.strip()
        ]

        input_string = "".join(expected_graphemes)
        TEST_CASES.append((input_string, expected_graphemes, description))

@pytest.mark.parametrize("input_string,expected_graphemes,description", TEST_CASES)
def test_default_grapheme_suit(input_string, expected_graphemes, description):
    print(input_string, expected_graphemes)
    assert list(grapheme.graphemes(input_string)) == expected_graphemes
    assert grapheme.length(input_string) == len(expected_graphemes)



