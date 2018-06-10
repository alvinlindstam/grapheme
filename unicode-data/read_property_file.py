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
            chardata[group_name]["single_chars"].append(start)
        else:
            chardata[group_name]["ranges"].append((start, end))

with open(os.path.join(dir_path, EMOJI_DATA_FILE), "r") as file:
    for line in file:
        match = pattern.search(line)
        if not match:
            continue

        (start, _, end, group_name) = match.groups()

        if group_name != "Extended_Pictographic":
            continue

        if end is None:
            chardata[group_name]["single_chars"].append(start)
        else:
            chardata[group_name]["ranges"].append((start, end))

        # print((start, end, group_name))
print(chardata.keys())
with open(os.path.join(dir_path, BREAK_PROPERTY_JSON_FILE), "w") as out_file:
    out_file.write(json.dumps(chardata, indent=2))
