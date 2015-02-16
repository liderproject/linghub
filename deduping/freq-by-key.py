import sys
from itertools import groupby
from collections import Counter
import re

write_uris = True
if len(sys.argv) > 1 and sys.argv[1] == "s":
    summary = True
elif len(sys.argv) > 1 and sys.argv[1] == "c":
    summary = False
    write_uris = False
else:
    summary = False


def is_significant(identifier):
    if identifier.startswith("<"):
        return bool(re.match("<(f|ht)tps?://.*/.+>", identifier))
    else:
        return len(identifier) >= 5


def extract_src(uri):
    x = uri.index("/", 33)
    return uri[33:x]


def src_freq(values):
    x = (extract_src(v) for v in set(values))
    return {key: len(list(group)) for key, group in groupby(x)}


by_pairs = Counter()


def by_pair(dictionary):
    for k1, v1 in dictionary.items():
        for k2, v2 in dictionary.items():
            if k1 < k2:
                by_pairs[k1 + "-" + k2] += v1 * v2
            if k1 == k2:
                by_pairs[k1] += v1 - 1


last = ""
values = set([])
for line in sys.stdin.readlines():
    elems = line.split("\t")
    if elems[0] != last:
        if len(values) > 1 and is_significant(last):
            if summary:
                by_pair(src_freq(values))
            elif write_uris:
                print("%s\t%s" % (last, " ".join(values)))
            else:
                print("%s\t%s" % (last, str(src_freq(values))))
        last = elems[0]
        values = set([elems[1].strip()])
    else:
        values.add(elems[1].strip())

if len(values) > 1 and is_significant(last):
    if summary:
        by_pair(src_freq(values))
    elif write_uris:
        print("%s\t%s" % (last, " ".join(values)))
    else:
        print("%s\t%s" % (last, str(src_freq(values))))

if summary:
    for k in by_pairs:
        print("%s %d" % (k, by_pairs[k]))
