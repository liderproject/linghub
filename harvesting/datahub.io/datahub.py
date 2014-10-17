import urllib
import urllib2
import json
import re
import math
import os

from urllib2 import HTTPError, URLError, Request, urlopen

# todos: 
# - check on runtime whether the URLs given are alive	# ok ... but now it's REALLY slow
# - check on runtime whether format is RDF or OWL		# for many dataset, the metadata is incomplete, e.g., dbpedia-ko, hence later

# meta data categories:
# via tags:
# "corpus" => llod:corpus
# "lexicon", "wordnet" => llod:corpus
# (none of these) => llod:language_description

if not os.path.exists("data"):
    os.mkdir("data")

baseURL = "http://datahub.io/api/3/action/"
blacklist = [
'masc', 																				# rdf export... not linked data
'apertium', 																			# not rdf
'wiktionary-en', 																		# not rdf
'wordnet', 																				# not rdf
'saldo', 																				# not rdf
'xwn', 																					# not rdf
'talkbank', 																			# not rdf
'french-timebank', 																		# not rdf
'jmdict', 																				# not rdf
'multext-east', 																		# not rdf
'wikiword_thesaurus', 																	# not rdf
'eu-dgt-tm', 																			# not rdf
'multilingualeulaw', 																	# not rdf
'wiktionary', 																			# not rdf
'omegawiki', 																			# not rdf
'framenet', 																			# not rdf
'o-anc', 																				# not rdf
'conceptnet', 																			# not rdf
'phoible', 																				# not rdf
'opus', 																				# not rdf
# 'sanskrit-english-lexicon', 															# down	# CC: checked at runtime
# 'pali-english-lexicon', 																# down	# CC: checked at runtime
'dbpedia-spotlight', 																	# tool not data!
'ss', 																					# spam
'cgsddforja', 																			# spam
'sqxfetge', 																			# spam
'fafqwfaf', 																			# spam
'sqxfetgea', 																			# spam
'printed-book-auction-catalogues' 														# spam ?
'analisi-del-blog-http-www-beppegrillo-it', 											# spam
'cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-expert-scrubs-for-safety' 	# spam
]

def ckanListDatasetsInGroup(group):
  url = baseURL + "group_list?id=" + group
  return json.loads(urllib2.urlopen(url).read())

def ckanListDatasetsForTag(tag):
  url = baseURL + "tag_show?id=" + tag
  return json.loads(urllib2.urlopen(url).read())
  
def ckanDataset(dataset):
  url = baseURL + "package_list?id=" + dataset
  return json.loads(urllib2.urlopen(url).read())

def rdfFromCkan(url):
    r = Request(url)
    r.add_header("Accept","application/rdf+xml")
    return urlopen(r).read()

nodes = {}

# NEW: check not only group data sets, but everything with a corresponding tag

#datasetJSON = ckanListDatasetsInGroup("linguistics")
#datasets = [ds["name"] for ds in datasetJSON["result"]["packages"]]	
#print "group 'linguistics': "+str(len(datasets))+" datasets"
datasets = []
for tag in ["llod", "linguistics%20lod", "lexicon", "corpus", "thesaurus", "isocat", "linguistic", "linguistics", "typology"]:
	 newDatasetJSON = ckanListDatasetsForTag (tag)
	 newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["packages"]]
	 datasets = datasets + newDatasets
	 datasets = list(set(datasets))
	 print "+ tag '"+tag+"': "+str(len(datasets))+" datasets"
		
datasets = set(datasets) - set(blacklist)
print "- blacklist: "+str(len(datasets))+" datasets"

for dataset in datasets:
  nodes[dataset] = {}
  nodes[dataset]["edgecount"] = 0

for dataset in datasets:
  print(dataset)
  rdf = rdfFromCkan("http://datahub.io./dataset/%s" % dataset)
  with open("data/%s.rdf" % dataset,"w") as out:
      out.write(rdf)
