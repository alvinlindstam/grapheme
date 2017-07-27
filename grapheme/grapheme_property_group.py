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

    RANGE_TREE = None
    for key, value in data.items():
        for range_ in value["ranges"]:
            new_node = LeafNode(
                int(range_[0], 16),
                int(range_[1], 16),
                GraphemePropertyGroup(key)
            )
            if RANGE_TREE:
                new_subtree = RANGE_TREE.add(new_node)
                if new_subtree:
                    RANGE_TREE = ContainerNode([RANGE_TREE, new_subtree])
            else:
                RANGE_TREE = ContainerNode([new_node])

    del data
