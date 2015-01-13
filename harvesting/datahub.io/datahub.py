import urllib2
import json
import os
from urllib2 import Request
from rdflib import Graph, BNode, RDFS, Namespace, URIRef, RDF


if not os.path.exists("data"):
    os.mkdir("data")

baseURL = "http://datahub.io/api/3/action/"
blacklist = [
    'ss', 																					# spam
    'cgsddforja', 																			# spam
    'sqxfetge', 																			# spam
    'fafqwfaf', 																			# spam
    'sqxfetgea', 																			# spam
    'printed-book-auction-catalogues', 														# spam ?
    """cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-
expert-scrubs-for-safety""" 	# spam
]


def ckanListDatasetsInGroup(group):
    url = baseURL + "group_show?id=" + group
    return json.loads(urllib2.urlopen(url).read())


def ckanListDatasetsForTag(tag):
    url = baseURL + "tag_show?id=" + tag
    return json.loads(urllib2.urlopen(url).read())


def rdfFromCkan(url):
    r = Request(url)
    r.add_header("Accept", "application/rdf+xml")
    g = Graph()
    g.parse(url)
    return g


def fixCkan(g, url):
    """Align the CKAN data with DataID"""
    VOID = Namespace("http://rdfs.org/ns/void#")
    n_linksets = 1
    for s, p, o in g:
        if isinstance(s, BNode) and p == RDF.value:
            label = g.objects(s, RDFS.label).next()
            if str(label) == "triples":
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
    return g

nodes = {}

# NEW: check not only group data sets, but everything with a corresponding tag

datasetJSON = ckanListDatasetsInGroup("owlg")
datasets = [ds["name"] for ds in datasetJSON["result"]["packages"]]
print "group 'owlg': "+str(len(datasets))+" datasets"
for group in ["mlode2012", "sfb673"]:
    newDatasetJSON = ckanListDatasetsInGroup(group)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["packages"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ group '"+group+"': "+str(len(datasets))+" datasets"
for tag in ["llod", "linguistics%20lod", "lexicon", "corpus", "thesaurus",
            "isocat", "linguistic", "linguistics", "typology", "lrec-2014",
            "lexical-resources"]:
    newDatasetJSON = ckanListDatasetsForTag(tag)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["packages"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ tag '"+tag+"': "+str(len(datasets))+" datasets"

datasets = set(datasets) - set(blacklist)
print "- blacklist: "+str(len(datasets))+" datasets"


for dataset in datasets:
    print(dataset)
    url = "http://datahub.io/dataset/%s" % dataset
    rdf = fixCkan(rdfFromCkan(url), url)
    with open("data/%s.rdf" % dataset, "w") as out:
        rdf.serialize(out)
