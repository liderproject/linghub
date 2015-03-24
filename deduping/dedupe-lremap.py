from rdflib import Graph, URIRef
from collections import Counter
from hashlib import md5
from math import tanh
import sys

g = Graph()

g.parse(sys.argv[1], format='nt')

title_dupes = {}
access_dupes = {}

accept_props = [
    URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
    URIRef("http://www.w3.org/ns/dcat#distribution")
]

for s, o in g.subject_objects(URIRef("http://purl.org/dc/elements/1.1/title")):
    title = o
    uri = s
    if title in title_dupes:
        title_dupes[title].add(uri)
    else:
        title_dupes[title] = set([uri])


for s, o in g.subject_objects(URIRef("http://www.w3.org/ns/dcat#accessURL")):
    access = o
    uri = str(s)
    uri = URIRef(uri[:uri.index('#')])
    if access in access_dupes:
        access_dupes[access].add(uri)
    else:
        access_dupes[access] = set([uri])

dupes = [v for k, v in title_dupes.items() + access_dupes.items()
         if len(v) > 1]

for i in range(0, len(dupes)):
    if i < len(dupes):
        d = dupes[i]
        for j in range(i + 1, len(dupes)):
            if j < len(dupes):
                d2 = dupes[j]
                i = d.intersection(d2)
                if len(i) != 0:
                    d.update(d2)
                    del dupes[j]

for d in dupes:
    ps = set([])
    for s in d:
        for p in g.predicates(s):
            ps.add(p)

    votes = Counter()
    for s in d:
        for o in g.objects(s, URIRef("http://purl.org/dc/elements/1.1/title")):
            votes[o] += 1
    if len(votes) > 0:
        title = max(votes, key=lambda x: -votes[x])
        m = md5()
        n = title.n3()
        m.update(n.encode('ascii', 'ignore'))
        new_s = URIRef("http://linghub.lider-project.eu/lremap/" + m.hexdigest())
        new_dist = URIRef("http://linghub.lider-project.eu/lremap/" +
                          m.hexdigest() + "#Distribution")

        for p in ps:
            if p == URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
                for o in g.objects(s, p):
                    g.add((new_s, p, o))
            elif p == URIRef("http://www.w3.org/ns/dcat#distribution"):
                votes = Counter()
                for o in g.objects(s, p):
                    for o2 in g.objects(
                            o, URIRef("http://www.w3.org/ns/dcat#accessURL")):
                        votes[o2] += 1
                if len(votes) > 0:
                    link = max(votes, key=lambda x: -votes[x])
                    g.add((new_s,
                           URIRef("http://www.w3.org/ns/dcat#distribution"),
                           new_dist))
                    g.add((new_dist,
                           URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                           URIRef("http://www.w3.org/ns/dcat#Distribution")))
                    g.add((new_dist,
                           URIRef("http://www.w3.org/ns/dcat#accessURL"),
                           link))
            else:
                votes = Counter()
                for s in d:
                    for o in g.objects(s, p):
                        votes[o] += 1
                new_o = max(votes, key=lambda x: - votes[x] - tanh(len(x)))
                g.add((new_s, p, o))

        for s in d:
            g.remove((s, None, None))
            s_dist = URIRef(s + "#Distribution")
            g.remove((s_dist, None, None))

g.serialize(sys.stdout, format='nt')
