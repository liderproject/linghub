#!/bin/bash

zcat ../harvesting/clarin/clarin.nt.gz | python extract-by-prop.py title | LC_ALL=C sort | python freq-by-key.py > dupes-by-title.tsv
python find-common-prefix.py < dupes-by-title.tsv > remapping-clarin.tsv
zcat ../harvesting/clarin/clarin.nt.gz | python remap-clarin.py | gzip > ../harvesting/clarin/clarin.deduped.nt.gz

