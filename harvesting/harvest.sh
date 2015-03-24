#!/bin/bash

LINGHUB=linghub.lider-project.eu

die() { echo "$@" 1>&2 ; exit 1; }

check() {
    command -v $1 > /dev/null || die "$1 is not installed"
}

clean() {
    rm -f linghub.nt.gz datahub.io/datahub.nt.gz lre-map/lremap.nt.gz metashare/metashare.nt.gz clarin/clarin.nt.gz 
    echo "Clean" 
}

compile() {
    rm -f linghub.nt.gz
    if [ -e clarin/clarin.deduped.nt.gz ]
    then
        CLARIN_NT_GZ=clarin/clarin.deduped.nt.gz
    else
        CLARIN_NT_GZ=clarin/clarin.nt.gz
    fi
    if [ -e metashare/metashare.deduped.nt.gz ]
    then
        METASHARE_NT_GZ=metashare/metashare.deduped.nt.gz
    else
        METASHARE_NT_GZ=metashare/metashare.nt.gz
    fi
    for f in datahub.io/datahub.nt.gz lre-map/lremap.nt.gz METASHARE_NT_GZ $CLARIN_NT_GZ 
    do
        zcat $f | python add_langs.py | gzip >> linghub.nt.gz
    done
    cd ../deduping
    bash dedupe-all.sh
    cd -
}

datahub() {
    echo "Starting export of DataHub"
    check "python" 
    check "rapper"
    check "perl"

    cd datahub.io/
    echo "Obtaining data [1/2]"
    if [ ! -d data ]
    then
        python datahub.py
    fi
    echo "Processing data [2/2]"
    cd data/
    for f in *.rdf
    do
        DATASET_NAME="${f/%.rdf/}"
        echo "Dataset: $DATASET_NAME"
        rapper -o ntriples $f 2>/dev/null | perl -p -e "s/http:\/\/datahub.io\/dataset/http:\/\/$LINGHUB\/datahub/g" | python ../fix-urls.py "http://$LINGHUB/datahub/$DATASET_NAME#" | gzip >> ../datahub.nt.gz
        echo "<http://$LINGHUB/datahub/$DATASET_NAME> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://datahub.io/dataset/$DATASET_NAME> . " | gzip >> ../datahub.nt.gz
        echo "<http://$LINGHUB/datahub/$DATASET_NAME> <http://purl.org/dc/elements/1.1/source> \"DataHub\" . " | gzip >> ../datahub.nt.gz

    done
    cd ../../
}

lremap() {
    echo "Starting export of LRE-Map"
    check "curl"
    check "python"
    check "rapper"

    cd lre-map/
    # For some reason this doesn't work with wget!
    #curl http://www.resourcebook.eu/lremap/owl/lremap.zip > lremap.zip || die "Could not download LRE-Map data"
    #mkdir data/
    #unzip lremap.zip -d data/
    #python lre-map.new.py
    #Give up Riccardo's RDF dump is currently too FUBAR

    ls -lh
    if [ ! -e lre-map.html ]
    then
        # zcat lre-map.html.gz > lre-map.html # zcat on OS X always appends a .Z to the filename (better use gunzip -c)
        gunzip -c lre-map.html.gz > lre-map.html
    fi
    echo "Building RDF [1/4]"
    python lre-map.html.py
    echo "Converting to NT [2/4]"
    rapper -o ntriples -I http://linghub.lider-project.eu/lremap/ lre-map.rdf 2>/dev/null | python lre-map-add-usages.py > lremap.nt
    echo "Removing Duplicates [3/4]"
    python ../../deduping/dedupe-lremap.py lremap.nt | gzip > lremap.nt.gz
    rm lre-map.rdf
    rm lre-map.html
    cd ..
    echo "Add 2014 Data [4/4]"
    cd lre-map2014
    python LRE-Map2014Harvester.py
    cat LREmap2014.nt | gzip >> ../lre-map/lremap.nt.gz
    cd ..
}

clarin() {
    echo "Starting export of CLARIN"
    check "wget"
    check "xsltproc"
    check "tar"
    check "rapper"

    cd clarin
    echo "Downloading Data [1/3]"
    wget http://catalog.clarin.eu/oai-harvester/resultsets/clarin.tar.bz2
    wget http://catalog.clarin.eu/oai-harvester/resultsets/others.tar.bz2

    echo "Extracting Data [2/3]"
    tar xjvf clarin.tar.bz2
    tar xjvf others.tar.bz2

    echo "Converting Data [3/3]"
    for f in `find results/cmdi -name \*.xml`
    do
        RES_NAME2=${f/%.xml/}
        RES_NAME=${RES_NAME2/#results\/cmdi\/}
        SOURCE=$(dirname "$RES_NAME")
        if grep -q DcmiTerms $f
        then
            echo "Resource: $RES_NAME"
            xsltproc clarin2dcat.xsl $f | rapper -o ntriples -I http://$LINGHUB/clarin/$RES_NAME - 2>/dev/null |  gzip >> clarin.nt.gz
            echo "<http://$LINGHUB/clarin/$RES_NAME> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://catalog.clarin.eu/oai-harvester/others/results/cmdi/$RES_NAME.xml> ." | gzip >> clarin.nt.gz
            echo "<http://$LINGHUB/clarin/$RES_NAME> <http://purl.org/dc/elements/1.1/source> \"${SOURCE//_/ } (via CLARIN VLO)\" ." | gzip >> clarin.nt.gz
        else
            echo "Skipping: $RES_NAME"
        fi
    done
    cd ..
}

metashare() {
    echo "Starting export of Metashare"
    check "java"
    check "rapper"

    cd metashare
    echo "Extracting Data [1/3]"
    if [ ! -d META-SHARE_LRs ]
    then
        unzip META-SHARE_LRs.zip
    fi

    echo "Running LIXR [2/3]"
    for f in META-SHARE_LRs/*.xml
    do
        java -jar lixr-assembly-0.1.jar metashare $f | rapper -i turtle -o ntriples -I http://$LINGHUB/metashare/ - | gzip >> metashare.nt.gz
    done

    echo "Deduping META-SHARE [3/3]"
    zcat metashare.nt.gz | python ../../deduping/metashare-dedupe.py | gzip > metashare.deduped.nt.gz

    cd ..
}

dataid() {
    cd dataid

    echo "Collecting DataID records"
    check "rapper"

    while read dataid; do
      curl -H "Accept: application/rdf+xml" $read | rapper -o ntriples -I http://$LINGHUB/dataid/ - | python fix_urls.py $read | gzip >> dataid.nt.gz
    done <sources.txt

    cd ..
}

case "$1" in
    all)
        clean
        datahub
        lremap
        metashare
        clarin
        compile
        ;;
    clean)
        clean
        ;;
    datahub)
        datahub
        ;;
    lremap)
        lremap
        ;;
    clarin)
        clarin
        ;;
    metashare)
        metashare
        ;;
    dataid)
        dataid
        ;;
    compile)
        compile
        ;;
    *) 
        echo "Please specify a stage (all|clean|datahub|clarin|lremap|metashare|dataid|compile)"
esac

            
