# Requires requests
#   sudo pip install requests
#import requests
#
#
# This doesn't work as resourcebook.eu is apparently barely functional
# Instead manually obtain the source for the page with Chrome at lre-map.html
#payload = {
#    "logged":"",
#    "passcode":"",
#    "searched":"true",
#    "buttonope":"",
#    "rps":"NoFilter",
#    "ravail":"NoFilter",
#    "languages":"none|none|none|none|none",
#    "resnames":"none|none|none|none|none",
#    "top":"",
#    "mop":"",
#    "mapRT":"",
#    "sbpForm":"",
#    "toolForm":"",
#    "firstTime":"1",
#    "isNosubmit":"1",
#    "RTFilter":"NoFilter",
#    "RT_other":"",
#    "langtype":"Any",
#    "reslangtype":"Not Relevant",
#    "RMFilter":"NoFilter",
#    "RM_other":"",
#    "RUFilter":"NoFilter",
#    "RU_other":"",
#    "RAFilter":"NoFilter",
#    "RA_other":"",
#    "RPSFilter":"NoFilter",
#    "RPS_other":""
#}
#
#r = requests.get("http://www.resourcebook.eu/searchll.php")#,data=payload)
#
#print r.text

import re
import json
from xml.sax.saxutils import escape
from urllib import quote

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def fix_url(url):
    for c in unicode(url):
        if ord(c) > 128:
            yield quote(c.encode('utf-8'))
        else:
            yield c

if __name__ == "__main__":
    found_debug = False
    resources = {}
    current_id = -1

    for line in open("lre-map.html").readlines():
        if "Debug" in line:
            found_debug = True
        if found_debug:
            m = re.match("^\s+\[(\d+)\] => Array\s+$", line)
            if m:
                current_id = int(m.group(1))
                resources[current_id] = {}
            else:
                m = re.match("^\s+\[(\w+)\] => (.*)$", line)
                if m and current_id != -1:
                    prop = m.group(1)
                    val = m.group(2)
                    resources[current_id][prop] = val

    with open("lre-map.rdf","w") as out:
        out.write("""<?xml version='1.0' encoding='utf-8'?>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:lre='http://www.resourcebook.eu/lremap/owl/lremap_resource.owl#' xmlns:dcat='http://www.w3.org/ns/dcat#' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:dct='http://purl.org/dc/terms/'>""")
        for key, data in resources.items():
            out.write("  <dcat:Dataset rdf:about='%s'>\n" % data["ID"])
            for p,v in data.items():
                # Hack as one field contains LF
                v = v.replace(chr(12),"?")
                if p == "License" and v != "":
                    out.write("    <dc:rights>%s</dc:rights>\n" % (escape(v)))
                elif p == "ResourceType" and v != "":
                    out.write("    <dc:type>%s</dc:type>\n" % (escape(v)))
                elif p == "Languages" and v != "":
                    out.write("    <dc:language>%s</dc:language>\n" % (escape(v)))
                elif p == "Year" and v != "":
                    out.write("    <dct:issued rdf:datatype=\"http://www.w3.org/2001/XMLSchema#gYear\">%s</dct:issued>\n" % (escape(v)))
                elif p == "ResourceName" and v != "":
                    out.write("    <dc:title>%s</dc:title>\n" % (escape(v)))
                elif p == "resourceUrl" and v != "":
                    if re.match(url_regex, v):
                        url = escape(''.join(fix_url(v)))
                        out.write("""    <dcat:distribution>
      <dcat:Distribution rdf:about='lre_%s#Distribution'>
        <dcat:accessURL rdf:resource=\"%s\"/>
      </dcat:Distribution>
    </dcat:distribution>
""" % (data["ID"], url))
                    else:
                        out.write("""    <dcat:distribution>
       <dcat:Distribution rdf:about='%s#Distribution'>
        <dcat:accessURL>%s</dcat:accessURL>
      </dcat:Distribution>
    </dcat:distribution>
""" % (data["ID"], escape(v)))
                        
                elif v != "":
                    out.write("    <lre:%s>%s</lre:%s>\n" % (p,escape(v),p))
            out.write("  </dcat:Dataset>\n")
        out.write("</rdf:RDF>")

