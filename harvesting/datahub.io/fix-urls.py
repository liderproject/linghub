import sys

fix_url = sys.argv[1]

for line in sys.stdin:
    e = line.strip().split(" ")

    if e[0].startswith("_:"):
        e[0] = "<%s>" % e[0].replace("_:",fix_url)
    if e[2].startswith("_:"):
        e[2] = "<%s>" % e[2].replace("_:",fix_url)
    print(" ".join(e))
