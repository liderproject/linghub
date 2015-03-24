#!/bin/bash

zcat ../harvesting/linghub.nt.gz | python extract-by-prop.py title | LC_ALL=C sort | python freq-by-key.py > dupes-by-title.tsv
python find-best.py < dupes-by-title.tsv | gzip >> ../harvesting/linghub.nt.gz
