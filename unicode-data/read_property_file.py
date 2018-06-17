import json
import os
import re
from collections import defaultdict


BREAK_PROPERTY_FILE = "GraphemeBreakProperty.txt"
EMOJI_DATA_FILE = "emoji-data.txt"
BREAK_PROPERTY_JSON_FILE = "../grapheme/data/grapheme_break_property.json"

pattern = re.compile("^([0-9A-F]+)(\.\.([0-9A-F]+))?\s+;\s*(\w*)\s*#")
dir_path = os.path.dirname(os.path.realpath(__file__))


class Group:
    single_chars = []
    ranges = []
def group():
    return dict(
        single_chars=[],
        ranges=[]
    )

chardata = defaultdict(group)

with open(os.path.join(dir_path, BREAK_PROPERTY_FILE), "r") as file:
    for line in file:
        if line.startswith("#"):
            continue

        match = pattern.search(line)
        if not match:
            continue

        (start, _, end, group_name) = match.groups()

        if end is None:
            chardata[group_name]["single_chars"].append(int(start, 16))
        else:
            chardata[group_name]["ranges"].append((int(start, 16), int(end, 16)))

with open(os.path.join(dir_path, EMOJI_DATA_FILE), "r") as file:
    for line in file:
        match = pattern.search(line)
        if not match:
            continue

        (start, _, end, group_name) = match.groups()

        if group_name != "Extended_Pictographic":
            continue

        if end is None:
            chardata[group_name]["single_chars"].append(int(start, 16))
        else:
            chardata[group_name]["ranges"].append((int(start, 16), int(end, 16)))

# Join adjacent ranges.
for group in chardata.values():
    last_max = None
    ranges = []
    for min_, max_ in list(sorted(group["ranges"])):
        if last_max and last_max + 1 == min_:
            ranges[-1][1] = max_
        else:
            ranges.append([min_, max_])
        last_max = max_

        for next_ in range(last_max + 1, last_max+100):
            if next_ in group["single_chars"]:
                group["single_chars"].remove(next_)
                ranges[-1][1] = next_
                last_max = next_
            else:
                break

        for prev in range(min_ - 1, 0, -1):
            if prev in group["single_chars"]:
                group["single_chars"].remove(prev)
                ranges[-1][0] = prev
            else:
                break
    group["ranges"] = ranges

with open(os.path.join(dir_path, BREAK_PROPERTY_JSON_FILE), "w") as out_file:
    out_file.write(json.dumps(chardata, indent=2))
