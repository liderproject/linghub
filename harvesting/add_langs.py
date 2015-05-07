import sys
import json
import re

# Inspite of the name also adds types!

def print_lang(uri, lang):
    print("%s <http://purl.org/dc/terms/language> "
          "<http://www.lexvo.org/id/iso639-3/%s> ." % (uri, lang))


def print_type(uri, lang):
    print("%s <http://purl.org/dc/terms/type> "
          "<http://babelnet.org/rdf/s%s> ." % (uri, lang))


def print_ms_type(uri, lang):
    sys.stderr.write("%s\n" % lang)
    print("%s <http://purl.org/dc/terms/type> "
          "<http://purl.org/net/def/metashare#%s> ." % (uri, lang))


langs = {}
lang_map = open("lang-map.json")
for line in lang_map.readlines():
    obj = json.loads(line)
    if "id" in obj and "rank" in obj and obj["rank"] >= 0.67:
        langs[obj["original"]] = obj["id"]

true_bnss = set([])
true_mn = set([])
bn_ns = {}
babelnet_types = open("babelnet-types.csv")
for line in babelnet_types.readlines():
    elems = line.strip().split(",")
    if elems[2] == "y":
        true_bnss.add(elems[0])
    if elems[3] != "":
        true_mn.add(elems[0])
        bn_ns[elems[0]] = elems[3]

bnss = {}
mns = {}
type_label_to_bnss = open("type-label-tobnss.tsv")
for line in type_label_to_bnss.readlines():
    elems = line.strip().split("\t")
    if elems[1] in true_bnss:
        if elems[0] not in bnss:
            bnss[elems[0]] = []
        bnss[elems[0]].append(elems[1])
    if elems[1] in true_mn:
        if elems[0] not in mns:
            mns[elems[0]] = []
        mns[elems[0]].append(bn_ns[elems[1]])

for line in sys.stdin:
    print(line.strip())
    elems = line.split(" ")
    if len(elems) > 2 and elems[1] == "<http://purl.org/dc/elements/1.1/language>":
        lang = (" ".join(elems[2:-1]))[1:-1]
        if lang in langs:
            print_lang(elems[0], langs[lang])
        else:
            for l in re.split("[,;]", lang):
                if l in langs:
                    print_lang(elems[0], langs[l])
    elif len(elems) > 2 and elems[1] == "<http://purl.org/dc/elements/1.1/type>":
        typ = (" ".join(elems[2:-1]))[1:-1]
        if typ in bnss:
            for bn in bnss[typ]:
                print_type(elems[0], bn[3:])
        if typ in mns:
            for mn in mns[typ]:
                print_ms_type(elems[0], mn)

