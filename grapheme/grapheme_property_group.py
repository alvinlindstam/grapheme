import json
import os
from enum import Enum


class GraphemePropertyGroup(Enum):
    PREPEND = "Prepend"
    CR = "CR"
    LF = "LF"
    CONTROL = "Control"
    EXTEND = "Extend"
    REGIONAL_INDICATOR = "Regional_Indicator"
    SPACING_MARK = "SpacingMark"
    L = "L"
    V = "V"
    T = "T"
    LV = "LV"
    LVT = "LVT"
    E_BASE = "E_Base"
    E_MODIFIER = "E_Modifier"
    ZWJ = "ZWJ"
    GLUE_AFTER_ZWJ = "Glue_After_Zwj"
    E_BASE_GAZ = "E_Base_GAZ"

    OTHER = "Other"


def get_group(char):
    return get_group_ord(ord(char))


def get_group_ord(char):
    for char_set, group in SINGLE_CHAR_MAPPINGS:
        if char in char_set:
            return group

    for lower_bound, upper_bound, group in RANGE_MAPPINGS:
        if lower_bound <= char <= upper_bound:
            return group

    return GraphemePropertyGroup.OTHER


# todo: should fix more efficient group lookup than this naive approach
with open(os.path.join(os.path.dirname(__file__), "data/grapheme_break_property.json"), 'r') as f:
    data = json.load(f)

    assert len(data) == len(GraphemePropertyGroup) - 1

    SINGLE_CHAR_MAPPINGS = [
        (
            set(int(char, 16) for char in value["single_chars"]),
            GraphemePropertyGroup(key)
        ) for key, value in data.items()
    ]

    RANGE_MAPPINGS = []
    for key, value in data.items():
        for range_ in value["ranges"]:
            RANGE_MAPPINGS.append((
                int(range_[0], 16),
                int(range_[1], 16),
                GraphemePropertyGroup(key)
            ))
    del data
