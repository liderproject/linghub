import sys
import json
import re


def print_lang(uri, lang):
    print("%s <http://purl.org/dc/terms/language> "
          "<http://www.lexvo.org/id/iso639-3/%s> ." % (elems[0], lang))


langs = {}
lang_map = open("lang-map.json")
for line in lang_map.readlines():
    obj = json.loads(line)
    if "id" in obj:
        langs[obj["original"]] = obj["id"]

for line in sys.stdin:
    print(line.strip())
    elems = line.split(" ")
    if elems[1] == "<http://purl.org/dc/elements/1.1/language>":
        lang = (" ".join(elems[2:-1]))[1:-1]
        if lang in langs:
            print_lang(elems[0], langs[lang])
        else:
            for l in re.split("[,;]", lang):
                if l in langs:
                    print_lang(elems[0], langs[l])
