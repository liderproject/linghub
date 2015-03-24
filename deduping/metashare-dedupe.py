import sys

titles = set()

cache = []

last = ""

# 0 = reading
# 1 = ignoring
# 2 = writing
state = 0


def head(s):
    if '#' in s:
        return s[:min(s.index('#'), s.index('>'))]
    else:
        return s[:s.index('>')]

for line in sys.stdin.readlines():
    elems = line.strip().split(" ")
    if last != head(line):
        for l in cache:
            sys.stdout.write(l)
        cache = []
        last = head(line)
        state = 0
    if elems[1] == "<http://purl.org/dc/elements/1.1/title>":
        title = " ".join(elems[2:])
        if title in titles and state == 0:
            cache = []
            state = 1
        else:
            for l in cache:
                sys.stdout.write(l)
            cache = []
            titles.add(title)
            state = 2
    if state == 0:
        cache.append(line)
    elif state == 1:
        pass
    else:
        sys.stdout.write(line)
