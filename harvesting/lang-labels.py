import sys

first = True

for line in sys.stdin.readlines():
    if first:
        first = False
    else:
        elems = line.strip().split("\t")
        print("<http://www.lexvo.org/id/iso639-3/%s> <http://www.w3.org/2000/01/rdf-schema#label> \"%s\"@en ." % (elems[0], elems[3]))
