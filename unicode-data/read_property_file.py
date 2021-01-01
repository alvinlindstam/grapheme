import json
import os
import re
from collections import defaultdict


BREAK_PROPERTY_FILE = "GraphemeBreakProperty.txt"
EMOJI_DATA_FILE = "emoji-data.txt"
BREAK_PROPERTY_JSON_FILE = "../grapheme/data/grapheme_break_property.json"

pattern = re.compile(r"^([0-9A-F]+)(\.\.([0-9A-F]+))?\s+;\s*(\w*)\s*#")
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

# Find characters with Extended_Pictographic flag from the emoji data file
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


for group in chardata.values():
    single_chars = group["single_chars"]
    ranges = []
    last_max = None
    for min_, max_ in sorted(group["ranges"]):
        # Extend range with adjacent single chars
        while min_ - 1 in single_chars:
            min_ -= 1
            single_chars.remove(min_)

        while max_ + 1 in single_chars:
            max_ += 1
            single_chars.remove(max_)

        # Join adjacent ranges.
        if last_max and last_max + 1 == min_:
            ranges[-1][1] = max_
        else:
            ranges.append([min_, max_])
        last_max = max_
    group["ranges"] = ranges


with open(os.path.join(dir_path, BREAK_PROPERTY_JSON_FILE), "w") as out_file:
    out_file.write(json.dumps(chardata, indent=2))
