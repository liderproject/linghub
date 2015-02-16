import sys

remap_file = open("remapping-clarin.tsv").readlines()
remap = {line.split("\t")[0]: line.strip().split("\t")[1]
         for line in remap_file}
remap_file = open("remapping-clarin.tsv").readlines()
remapfrag = {line.split("\t")[0]: line.strip().split("\t")[2]
             for line in remap_file}

def do_remap(uri):
    if uri in remap:
        return remap[uri]
    elif '#' in uri:
        short = uri[:uri.index('#')] + ">"
        frag = uri[uri.index('#') + 1:]
        if short in remap:
            return "%s#%s" % (remap[short][:-1], frag)
        else:
            return uri
    else:
        return uri


for line in sys.stdin.readlines():
    elems = line.strip().split(" ")
    subj = do_remap(elems[0])
    prop = elems[1]
    obj = " ".join(elems[2:-1])
    if obj.startswith("<"):
        obj = do_remap(obj)

    print("%s %s %s ." % (subj, prop, obj))
