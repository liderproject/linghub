#!/bin/bash

LINGHUB=linghub.lider-project.eu

die() { echo "$@" 1>&2 ; exit 1; }

check() {
    command -v $1 > /dev/null || die "$1 is not installed"
}

clean() {
    if [ -e linghub.nt.gz ] 
    then
        rm linghub.nt.gz
    fi
    touch linghub.nt.gz
    echo "Clean" 
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
        rapper -o ntriples $f 2>/dev/null | perl -p -e 's/http\/\/datahub.io\/dataset/http:\/\/$LINGHUB\/datahub/g' | python ../fix-urls.py "http://$LINGHUB/datahub/$DATASET_NAME#" | gzip >> ../../linghub.nt.gz
        echo "<http://$LINGHUB/datahub/$DATASET_NAME> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://datahub.io/dataset/$DATASET_NAME> . " | gzip >> ../../linghub.nt.gz

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

    if [ ! -e lre-map.html ]
    then
        zcat lre-map.html.gz > lre-map.html
    fi
    echo "Building RDF [1/2]"
    python lre-map.html.py
    echo "Converting to NT [2/2]"
    rapper -o ntriples -I http://linghub.lider-project.eu/lremap/ lre-map.rdf 2>/dev/null | gzip >> ../linghub.nt.gz
    rm lre-map.rdf
    rm lre-map.html
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
        echo "Resource: $RES_NAME"
        xsltproc clarin2dcat.xsl $f | rapper -o ntriples -I http://$LINGHUB/clarin/$RES_NAME - 2>/dev/null |  gzip >> ../linghub.nt.gz
        echo "<http://$LINGHUB/clarin/$RES_NAME> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://catalog.clarin.eu/oai-harvester/others/results/cmdi/$RES_NAME.xml> ." | gzip >> ../linghub.nt.gz
    done
    cd ..
}

metashare() {
    echo "Starting export of Metashare"
    check "java"
    check "rapper"

    cd metashare
    echo "Extracting Data [1/2]"
    if [ ! -d META-SHARE_LRs ]
    then
        unzip META-SHARE_LRs.zip
    fi

    echo "Running LIXR [2/2]"
    for f in META-SHARE_LRs/*.xml
    do
        java -jar lixr-assembly-0.1.jar metashare $f | rapper -i turtle -o ntriples -I http://$LINGHUB/metashare/ - | gzip >> ../linghub.nt.gz
    done

    cd ..
}

case "$1" in
    all)
        clean
        datahub
        lremap
        metashare
        clarin
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
    *) 
        echo "Please specify a stage (all|clean|datahub|clarin|lremap|metashare)"
esac

            
