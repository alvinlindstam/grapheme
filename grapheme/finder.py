from grapheme import GraphemePropertyGroup as G
from grapheme import get_group


def graphemes(string):
    assert isinstance(string, str)

    buffer = string[0]
    current_group = get_group(buffer)

    for codepoint in string[1:]:
        prev_group = current_group
        current_group = get_group(codepoint)

        if should_break(prev_group, current_group):
            yield buffer
            buffer = codepoint
        else:
            buffer += codepoint

    if buffer:
        yield buffer

    raise StopIteration()


def should_break(prev, next_):
    if prev is G.CR and next_ is G.LF:
        return False
    if prev in [G.CONTROL, G.CR, G.LF]:
        return True
    if prev in [G.CONTROL, G.CR, G.LF]:
        return True

    if prev is G.L and next_ in [G.L, G.V, G.LV, G.LVT]:
        return False
    if prev in [G.LV, G.V] and next_ in [G.V, G.T]:
        return False
    if prev in [G.LVT, G.T] and next_ is G.T:
        return False

    if next_ in [G.EXTEND, G.ZWJ]:
        return False

    if next_ is G.SPACING_MARK:
        return False

    if prev is G.PREPEND:
        return False

    # todo: handle extend
    if prev in [G.E_BASE, G.E_BASE_GAZ] and next_ is G.E_MODIFIER:
        return False
    if prev is G.ZWJ and next_ in [G.GLUE_AFTER_ZWJ, G.E_BASE_GAZ]:
        return False

    # todo: handle batches of two G.REGIONAL_INDICATOR
    if prev is G.REGIONAL_INDICATOR and next_ is G.REGIONAL_INDICATOR:
        return False

    return True
