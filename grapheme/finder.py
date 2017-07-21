from grapheme import GraphemePropertyGroup as G
from grapheme import get_group


class IterationFlags:
    def __init__(self):
        self.is_in_emoji = False
        self.did_just_break_on_regional_indicator = False

def graphemes(string):
    assert isinstance(string, str)

    iteration_flags = IterationFlags()

    buffer = string[0]
    current_group = get_group(buffer)

    for codepoint in string[1:]:
        prev_group = current_group
        current_group = get_group(codepoint)

        if should_break(prev_group, current_group, iteration_flags):
            yield buffer
            buffer = codepoint
        else:
            buffer += codepoint

    if buffer:
        yield buffer

    raise StopIteration()


def should_break(prev, next_, iteration_flags):
    # Handle special case of lookback in flags
    if prev is G.REGIONAL_INDICATOR and next_ is G.REGIONAL_INDICATOR and not iteration_flags.did_just_break_on_regional_indicator:
        iteration_flags.did_just_break_on_regional_indicator = True
        return False
    iteration_flags.did_just_break_on_regional_indicator = False

    if iteration_flags.is_in_emoji:
        if next_ is G.EXTEND:
            return False
        iteration_flags.is_in_emoji = False
        if next_ is G.E_MODIFIER:
            return False

    if prev is G.CR and next_ is G.LF:
        return False
    if prev in [G.CONTROL, G.CR, G.LF]:
        return True
    if next_ in [G.CONTROL, G.CR, G.LF]:
        return True

    if prev is G.L and next_ in [G.L, G.V, G.LV, G.LVT]:
        return False
    if prev in [G.LV, G.V] and next_ in [G.V, G.T]:
        return False
    if prev in [G.LVT, G.T] and next_ is G.T:
        return False

    if next_ in [G.EXTEND, G.ZWJ]:
        if prev in [G.E_BASE, G.E_BASE_GAZ]:
            iteration_flags.is_in_emoji = True
        return False

    if next_ is G.SPACING_MARK:
        return False

    if prev is G.PREPEND:
        return False

    if prev in [G.E_BASE, G.E_BASE_GAZ] and next_ is G.E_MODIFIER:
        return False

    if prev is G.ZWJ and next_ in [G.GLUE_AFTER_ZWJ, G.E_BASE_GAZ]:
        return False

    return True
