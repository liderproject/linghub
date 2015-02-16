import sys
from urllib import quote_plus


for line in sys.stdin.readlines():
    elems = line.strip().split("\t")
    uris = elems[1].split(" ")
    substr = uris[0][:-1]
    valid = True
    for i in range(1, len(uris)):
        try:
            idx = (j for j in range(0, min(len(substr), len(uris[i])))
                   if substr[j] != uris[i][j]).next()
            substr = substr[:idx]
            valid = valid and "/" not in uris[i][idx:]
        except StopIteration:
            pass
    common_uri = substr + quote_plus(elems[0][1:-1])
    if valid:
        for uri in uris:
            if len(substr) != len(uri) - 1:
                print("%s\t%s>\t%s" % (uri, common_uri, uri[len(substr):-1]))
