import urllib2
import json
import os
import re
from urllib2 import Request
from rdflib import Graph, BNode, RDFS, Namespace, URIRef, RDF, Literal

DCT = Namespace("http://purl.org/dc/terms/")

if not os.path.exists("data"):
    os.mkdir("data")

baseURL = "https://old.datahub.io/api/3/action/"
blacklist = [
    'ss', 																					# spam
    'cgsddforja', 																			# spam
    'sqxfetge', 																			# spam
    'fafqwfaf', 																			# spam
    'sqxfetgea', 																			# spam
    """cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-
expert-scrubs-for-safety""" 	# spam
]

def url2json(url):
    return json.loads(urllib2.urlopen(urllib2.Request(url, headers={'User-Agent': 'python'})).read())


def ckanListDatasetsInGroup(group):
    url = baseURL + "package_search?rows=200&fq=organization:" + group
    return url2json(url)


def ckanListDatasetsForTag(tag):
    #url = baseURL + "tag_show?id=" + tag
    url = baseURL + "package_search?rows=200&fq=tags:" + tag
    return url2json(url)

def rdfFromCkan(url):
    r = Request(url)
    r.add_header("Accept", "application/rdf+xml")
    g = Graph()
    g.parse(url)
    return g


def fixCkan(g2, url):
    """Align the CKAN data with DataID"""
    VOID = Namespace("http://rdfs.org/ns/void#")
    g = Graph()
    for s, p, o in g2:
        g.add((s, p, o))
    n_linksets = 1
    for s, p, o in g2:
        if p == DCT.description and isinstance(o, Literal):
            o = Literal(re.sub("<br/?>", "\n", o.value))
            g.remove((s, DCT.description, None))
            g.add((s, DCT.description, o))
        if isinstance(s, BNode) and p == RDF.value:
            try:
                if len(list(g.objects(s, RDFS.label))) != 1:
                    for o in g.objects(s, RDFS.label):
                        print(s + " " + o)
                label = g.objects(s, RDFS.label).next()
            except:
                pass
            if str(label) == "triples":
                print(str(label))
                print(o)
                g.add((URIRef(url), VOID.triples, o))
                g.remove((None, None, s))
                g.remove((s, None, None))
            elif label.startswith("links:"):
                linkset = URIRef(url + "#LinkSet-" + str(n_linksets))
                g.add((URIRef(url), VOID.subset, linkset))
                g.add((linkset, VOID.triples, o))
                g.add((linkset, RDF.type, VOID.LinkSet))
                g.add((linkset, VOID.target,
                       URIRef("http://linghub.lider-project.eu/datahub/" +
                              label[6:])))
                n_linksets += 1
                g.remove((None, None, s))
                g.remove((s, None, None))
            elif str(label) == "license":
                g.add((URIRef(url), DCT.license, URIRef(str(o))))
                g.remove((None, None, s))
                g.remove((s, None, None))
    return g

nodes = {}

# NEW: check not only group data sets, but everything with a corresponding tag

datasetJSON = ckanListDatasetsInGroup("owlg")
datasets = [ds["name"] for ds in datasetJSON["result"]["results"]] + ["dbpedia"]
print "group 'owlg': "+str(len(datasets))+" datasets"
for group in ["mlode2012", "sfb673"]:
    newDatasetJSON = ckanListDatasetsInGroup(group)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["results"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ group '"+group+"': "+str(len(datasets))+" datasets"
for tag in ["llod", "linguistics%20lod", "lexicon", "corpus", "thesaurus",
            "isocat", "linguistic", "linguistics", "typology", "lrec-2014",
            "lexical-resources"]:
    newDatasetJSON = ckanListDatasetsForTag(tag)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["results"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ tag '"+tag+"': "+str(len(datasets))+" datasets"

datasets = set(datasets) - set(blacklist)
print "- blacklist: "+str(len(datasets))+" datasets"

for dataset in datasets:
    print(dataset)
    url = "https://old.datahub.io/dataset/%s.rdf" % dataset
    rdf = fixCkan(rdfFromCkan(url), url)
    with open("data/%s.rdf" % dataset, "w") as out:
        rdf.serialize(out)
