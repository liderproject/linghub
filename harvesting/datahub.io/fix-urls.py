import sys

fix_url = sys.argv[1]
dct = "<http://purl.org/dc/terms/"
dcelems = ["contributor", "coverage>", "creator>", "date>", "description>", 
           "format>", "identifier>", "language>", "publisher>", "relation>", 
           "rights>", "source>", "subject>", "title>", "type>"]

for line in sys.stdin:
    e = line.strip().split(" ")

    if e[0].startswith("_:"):
        e[0] = "<%s>" % e[0].replace("_:",fix_url)
    if e[1].startswith(dct) and e[1][len(dct):] in dcelems:
        e[1] = "<http://purl.org/dc/elements/1.1/" + e[1][len(dct):]
    if e[2].startswith("_:"):
        e[2] = "<%s>" % e[2].replace("_:",fix_url)
    print(" ".join(e))
