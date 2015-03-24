import sys

prefix_len = len("<http://linghub.lider-project.eu/")

order = ["metashare", "clarin", "datahub", "lremap"]

for line in sys.stdin.readlines():
    title, uris = line.strip().split("\t")
    resources = [(uri[prefix_len:], uri) for uri in uris.split(" ")]
    resources = [(uri[:uri.index('/')], uri2) for uri, uri2 in resources]
    m = min(order.index(uri) for uri, uri2 in resources)
    for resource, uri in resources:
        o1 = order.index(resource)
        for resource2, uri2 in resources:
            o2 = order.index(resource2)
            if o1 < o2 and o1 == m:
                print("%s <http://purl.org/dc/terms/isReplacedBy> %s ." %
                      (uri2, uri))
