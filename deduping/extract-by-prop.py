import sys
import re

both = False
if sys.argv[1] == "title":
    uri = "<http://purl.org/dc/elements/1.1/title>"
    frag = False
elif sys.argv[1] == "both":
    uri1 = "<http://purl.org/dc/elements/1.1/title>"
    uri2 = "<http://www.w3.org/ns/dcat#accessURL>"
    both = True
else:
    uri = "<http://www.w3.org/ns/dcat#accessURL>"
    frag = True

titles = {}
uris = {}

for line in sys.stdin.readlines():
    elems = line.split(" ")
    if len(elems) <= 2:
        continue
    ob = " ".join(elems[2:-1]).replace("\t", " ").lower()
    if re.match("(.*)@[A-Za-z0-9\-]+$", ob):
        ob = re.match("(.*)@[A-Za-z0-9\-]+$", ob).group(1)
    if '#' in elems[0]:
        s = elems[0][:elems[0].index('#')] + ">"
    else:
        s = elems[0]

    if both:
        if elems[1] == uri1 and "#" not in elems[0]:
            if not re.match(".*no title.*", ob, re.I):
                if s in uris:
                    print("%s%s\t%s" % (ob, uris[s], s))
                    del uris[s]
                else:
                    titles[s] = ob
        elif elems[1] == uri2 and ob.startswith("<"):
            if s in titles:
                print("%s%s\t%s" % (titles[s], ob, s))
                del titles[s]
            else:
                uris[elems[0]] = ob
    else:
        if elems[1] == uri and ((frag and ob.startswith("<"))
                                or (not frag and "#" not in elems[0])):
            if frag or not re.match(".*no title.*", ob, re.I):
                print("%s\t%s" % (ob, s))
