from enum import Enum

from grapheme.grapheme_property_group import GraphemePropertyGroup as G
from grapheme.grapheme_property_group import get_group


class FSM:
    @classmethod
    def default(cls, n):
        if n is G.OTHER:
            return True, cls.default

        if n is G.CR:
            return True, cls.cr

        if n in [G.LF, G.CONTROL]:
            return True, cls.lf_or_control

        if n in [G.EXTEND, G.SPACING_MARK, G.ZWJ]:
            return False, cls.default

        if n is G.EXTENDED_PICTOGRAPHIC:
            return True, cls.emoji

        if n is G.REGIONAL_INDICATOR:
            return True, cls.ri

        if n is G.L:
            return True, cls.hangul_l

        if n in [G.LV, G.V]:
            return True, cls.hangul_lv_or_v

        if n in [G.LVT, G.T]:
            return True, cls.hangul_lvt_or_t

        if n is G.PREPEND:
            return True, cls.prepend

        return True, cls.default

    @classmethod
    def default_next_state(cls, n, should_break):
        _, next_state = cls.default(n)
        return should_break, next_state

    @classmethod
    def cr(cls, n):
        if n is G.LF:
            return False, cls.lf_or_control
        return cls.default_next_state(n, should_break=True)

    @classmethod
    def lf_or_control(cls, n):
        return cls.default_next_state(n, should_break=True)

    @classmethod
    def prepend(cls, n):
        if n in [G.CONTROL, G.LF]:
            return True, cls.default
        if n is G.CR:
            return True, cls.cr
        return cls.default_next_state(n, should_break=False)

    # Hanguls
    @classmethod
    def hangul_l(cls, n):
        if n in [G.V, G.LV]:
            return False, cls.hangul_lv_or_v
        if n is G.LVT:
            return False, cls.hangul_lvt_or_t
        if n is G.L:
            return False, cls.hangul_l
        return cls.default(n)

    @classmethod
    def hangul_lv_or_v(cls, n):
        if n is G.V:
            return False, cls.hangul_lv_or_v
        if n is G.T:
            return False, cls.hangul_lvt_or_t
        return cls.default(n)

    @classmethod
    def hangul_lvt_or_t(cls, n):
        if n is G.T:
            return False, cls.hangul_lvt_or_t
        return cls.default(n)

    # Emojis
    @classmethod
    def emoji(cls, n):
        if n is G.EXTEND:
            return False, cls.emoji
        if n is G.ZWJ:
            return False, cls.emoji_zjw
        return cls.default(n)

    @classmethod
    def emoji_zjw(cls, n):
        if n is G.EXTENDED_PICTOGRAPHIC:
            return False, cls.emoji
        return cls.default(n)

    # Regional indication (flag)
    @classmethod
    def ri(cls, n):
        if n is G.REGIONAL_INDICATOR:
            return False, cls.default
        return cls.default(n)

class BreakPossibility(Enum):
    CERTAIN = "certain"
    POSSIBLE = "possible"
    NO_BREAK = "nobreak"


def get_break_possibility(a, b):
    # Probably most common, included as short circuit before checking all else
    if a is G.OTHER and b is G.OTHER:
        return BreakPossibility.CERTAIN

    assert isinstance(a, G)
    assert isinstance(b, G)

    # Only break if preceeded by an uneven number of REGIONAL_INDICATORS
    # sot (RI RI)* RI × RI
    # [ ^ RI] (RI RI) * RI    ×    RI
    if a is G.REGIONAL_INDICATOR and b is G.REGIONAL_INDICATOR:
        return BreakPossibility.POSSIBLE

    # (Control | CR | LF) ÷
    #  ÷ (Control | CR | LF)
    if a in [G.CONTROL, G.CR, G.LF] or b in [G.CONTROL, G.CR, G.LF]:
        # CR × LF
        if a is G.CR and b is G.LF:
            return BreakPossibility.NO_BREAK
        else:
            return BreakPossibility.CERTAIN

    # L × (L | V | LV | LVT)
    if a is G.L and b in [G.L, G.V, G.LV, G.LVT]:
        return BreakPossibility.NO_BREAK

    # (LV | V) × (V | T)
    if a in [G.LV, G.V] and b in [G.V, G.T]:
        return BreakPossibility.NO_BREAK

    # (LVT | T)    ×    T
    if a in [G.LVT, G.T] and b is G.T:
        return BreakPossibility.NO_BREAK

    # × (Extend | ZWJ)
    # × SpacingMark
    # Prepend ×
    if b in [G.EXTEND, G.ZWJ, G.SPACING_MARK] or a is G.PREPEND:
        return BreakPossibility.NO_BREAK

    # \p{Extended_Pictographic} Extend* ZWJ × \p{Extended_Pictographic}
    if a is G.ZWJ and b is G.EXTENDED_PICTOGRAPHIC:
        return BreakPossibility.POSSIBLE

    # everything else, assumes all other rules are included above
    return BreakPossibility.CERTAIN


def get_last_certain_break_index(string, index):
    if index >= len(string):
        return len(string)

    prev = get_group(string[index])
    while True:
        if index <= 0:
            return 0
        index -= 1
        cur = get_group(string[index])
        if get_break_possibility(cur, prev) == BreakPossibility.CERTAIN:
            return index + 1
        prev = cur


class GraphemeIterator:
    def __init__(self, string):
        self.str_iter = iter(string)
        try:
            self.buffer = next(self.str_iter)
        except StopIteration:
            self.buffer = None
        else:
            _, state = FSM.default(get_group(self.buffer))
            self.state = state

    def __iter__(self):
        return self

    def __next__(self):
        for codepoint in self.str_iter:
            should_break, state = self.state(get_group(codepoint))
            self.state = state

            if should_break:
                return self._break(codepoint)
            self.buffer += codepoint

        if self.buffer:
            return self._break(None)

        raise StopIteration()

    def _break(self, new):
        old_buffer = self.buffer
        self.buffer = new
        return old_buffer
