import json
import os
import string
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
    ZWJ = "ZWJ"
    EXTENDED_PICTOGRAPHIC = "Extended_Pictographic"

    OTHER = "Other"

COMMON_OTHER_GROUP_CHARS = ""

def get_group(char):
    if char in COMMON_OTHER_GROUP_CHARS:
        return GraphemePropertyGroup.OTHER
    else:
        return get_group_ord(ord(char))


def get_group_ord(char):
    group = SINGLE_CHAR_MAPPINGS.get(char, None)
    if group:
        return group

    return RANGE_TREE.get_value(char) or GraphemePropertyGroup.OTHER


class ContainerNode:
    """
    Simple implementation of interval based BTree with no support for deletion.
    """
    def __init__(self, children):
        self.children = self._sorted(children)
        self._set_min_max()

    def _set_min_max(self):
        self.min = self.children[0].min
        self.max = self.children[-1].max

    # Adds an item to the node or it's subnodes. Returns a new node if this node is split, or None.
    def add(self, item):
        for child in self.children:
            if child.min <= item.min <= child.max:
                assert child.min <= item.max <= child.max
                new_child = child.add(item)
                if new_child:
                    return self._add_child(new_child)
                else:
                    self._set_min_max()
                    return None
        return self._add_child(item)

    def get_value(self, key):
        for child in self.children:
            if child.min <= key <= child.max:
                return child.get_value(key)
        return None

    def _add_child(self, child):
        self.children.append(child)
        self.children = self._sorted(self.children)
        other = None
        if len(self.children) >= 4:
            other = ContainerNode(self.children[2:])
            self.children = self.children[0:2]
        self._set_min_max()
        return other

    def _sorted(self, children):
        return sorted(children, key=lambda c: c.min)


class LeafNode:
    def __init__(self, range_min, range_max, group):
        self.min = range_min
        self.max = range_max
        self.group = group

    # Assumes range check has already been done
    def get_value(self, _key):
        return self.group

with open(os.path.join(os.path.dirname(__file__), "data/grapheme_break_property.json"), 'r') as f:
    data = json.load(f)

    assert len(data) == len(GraphemePropertyGroup) - 1

    SINGLE_CHAR_MAPPINGS = {}

    for key, value in data.items():
        group = GraphemePropertyGroup(key)
        for char in value["single_chars"]:
            SINGLE_CHAR_MAPPINGS[char] = group

    RANGE_TREE = None
    for key, value in data.items():
        for range_ in value["ranges"]:
            min_ = range_[0]
            max_ = range_[1]
            group = GraphemePropertyGroup(key)
            if max_ - min_ < 20:
                for i in range(min_, max_ + 1):
                    SINGLE_CHAR_MAPPINGS[i] = group
                continue
            new_node = LeafNode( min_, max_, group)
            if RANGE_TREE:
                new_subtree = RANGE_TREE.add(new_node)
                if new_subtree:
                    RANGE_TREE = ContainerNode([RANGE_TREE, new_subtree])
            else:
                RANGE_TREE = ContainerNode([new_node])

    common_ascii = string.ascii_letters + string.digits + string.punctuation
    COMMON_OTHER_GROUP_CHARS = "".join(c for c in common_ascii if get_group(c) == GraphemePropertyGroup.OTHER)
    del data
