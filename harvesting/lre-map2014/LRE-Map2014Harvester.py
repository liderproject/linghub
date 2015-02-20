#!/usr/bin/python
#
#I got data about resources and conferences(lremap_ri.n3,lremap_conf.n3) from http://www.resourcebook.eu/lremap/owl/lremap.zip
#http://datahub.io/organization/institute-for-computational-linguistics-ilc-cnr
# Information about papers http://www.resourcebook.eu/lremap/owl/lremap_paper (need to be transformed in to n-triples)
#Information about submissions http://www.resourcebook.eu/lremap/owl/lremap_sub (need to be transformed in to n-triples)
#I used this tool (https://github.com/szydan/any23tool.git) to convert from RDF/XML to n-triples 
#http://www.resourcebook.eu/lremap/owl/lremap_ri is the same as lremap_ri.n3, only thing that lremap_ri.n3 is already in n-triple format
#http://www.resourcebook.eu/lremap/owl/lremap_conf is the same as lremap_conf.n3, only thing that lremap_conf.n3 is already in n-triple format
#
import re
import os
import sys
def cleaner(line):
    temp = line.replace('##','').replace('lremap_ri#','lremap_ri/').replace('/#','/').replace('lremap_paper#','lremap_paper/').replace('dcmitype//','dcmitype/')
    return temp

def changeSubmision(submisionsDic,line):
    searchObj = re.search( r'(<http://www.resourcebook.eu/lremap/owl/lremap_ri/)([^>]*)(> <http://purl.org/dc/terms/references> )(<http://www.resourcebook.eu/lremap/owl/lremap_sub#)([^>]*)(>.*)', line, re.M|re.I)
    if searchObj:
        if submisionsDic.has_key(searchObj.group(5)):
            temp = submisionsDic.get(searchObj.group(5))
            temp.append(searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(5))
            submisionsDic[searchObj.group(5)] = temp
        else:
            submisionsDic[searchObj.group(5)] = [searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(5)]
        output=searchObj.group(1)+searchObj.group(2)+searchObj.group(3)+searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(5)+searchObj.group(6)+'\n' 
    else:
        output=line
    return output  
 
def changePaper(paperDic,line):
    searchObj = re.search( r'(<http://www.resourcebook.eu/lremap/owl/lremap_ri/)([^>]*)(#[^>]*)(> <http://purl.org/dc/terms/references> )(<http://www.resourcebook.eu/lremap/owl/lremap_paper/)([^>]*)(.*)', line, re.M|re.I)
   # print line
    if searchObj:
        if paperDic.has_key(searchObj.group(6)):
            temp = paperDic.get(searchObj.group(6))
            temp.append(searchObj.group(1)+searchObj.group(2)+searchObj.group(6))
            paperDic[searchObj.group(6)] = temp
        else:
            paperDic[searchObj.group(6)] = [searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(6)]
        #output=searchObj.group(1)+searchObj.group(2)+searchObj.group(3)+searchObj.group(4)+searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(6)+searchObj.group(7)+'\n' 
        output=searchObj.group(1)+searchObj.group(2)+searchObj.group(3)+'> <http://swrc.ontoware.org/ontology#publication> '+searchObj.group(1)+searchObj.group(2)+'#'+searchObj.group(6)+searchObj.group(7)+'\n' 
        
    else:
        output=line
    return output

def changeConf(conferenceDic,line):
    searchObj = re.search( r'(<http://www.resourcebook.eu/lremap/owl/lremap_ri/)([^>]*)(#[^>]*)(> <http://purl.org/dc/terms/references> )(<http://www.resourcebook.eu/lremap/owl/lremap_conf)([^>]*)(.*)', line, re.M|re.I)
    if searchObj:
        if conferenceDic.has_key(searchObj.group(6)):
            temp = conferenceDic.get(searchObj.group(6))
            temp.append('<http://data.semanticweb.org/ns/swc/ontology'+searchObj.group(6))
            conferenceDic[searchObj.group(6)] = temp
        else:
            conferenceDic[searchObj.group(6)] = ['<http://data.semanticweb.org/ns/swc/ontology'+searchObj.group(6)] 
        #output=searchObj.group(1)+searchObj.group(2)+searchObj.group(3)+searchObj.group(4)+'<http://data.semanticweb.org/ns/swc/ontology'+searchObj.group(6)+searchObj.group(7)+'\n' 
        output=searchObj.group(1)+searchObj.group(2)+searchObj.group(3)+'> <http://purl.org/ontology/bibo/presentedAt> '+'<http://data.semanticweb.org/ns/swc/ontology'+searchObj.group(6)+searchObj.group(7)+'\n' 
    else:
        output=line
    return output     

def convertToTitle(line):
    #searchObj = re.search( r'(.*)(<http://www.resourcebook.eu/lremap/owl/lremap_resource.owl#hasResourceName> )(<http://www.resourcebook.eu/lremap/owl/lremap_ri#)([^>]*)(>.*)', line, re.M|re.I)
    searchObj = re.search( r'(<[^<]*)(<http://www.resourcebook.eu/lremap/owl/lremap_resource.owl#hasResourceName> )(<http://www.resourcebook.eu/lremap/owl/lremap_ri/)([^>]*)(>.*)', line, re.M|re.I)
    if searchObj:
        output = searchObj.group(1)+'<http://purl.org/dc/elements/1.1/title> '+ '\"'+searchObj.group(4).replace("_"," ")+'\"'+' .\n' 
    else:
        output = line
    return output


def main():
    tmpFile = open("tmp.nt", "wb")
    outFile = open(outputFilename, "wb") 
   
   
 #   if len(sys.argv) < 2:
 #       sys.stderr.write(' usage: pdf2text.py <pdffiles...>\n')
 #       exit(1)
 
 #Reads and processes resource file
    with open(resourceFilename, 'r') as resourceFile:
        submisionsDic = {}
        paperDic = {}
        conferenceDic = {}
        for line in resourceFile:
            tmpFile.write(convertToTitle(changeSubmision(submisionsDic,cleaner(line))))
        submisionsKeys = submisionsDic.keys()
 #Reads and processes submission file
    with open(submissionFilename, 'r') as submisionFile:    
        for line in submisionFile:
            temp = line.split(' ',1)
            temp2 = temp[0].split('#',1)
            if len(temp2) >1:
                tempkey = temp2[1].replace('>','')
                if submisionsDic.has_key(tempkey):
                    for prefix in submisionsDic[tempkey]:
                        output= prefix + '> ' + temp[1]
                        tempText = changeConf(conferenceDic,changePaper(paperDic,cleaner(output)))
                        text = tempText.replace('<http://purl.org/dc/dcmitype/Event>','<http://purl.org/ontology/bibo/Conference>')    
                        tmpFile.write(text)
# We don't need submission that are not connected to resources
#                else: 
#                    tmpFile.write(changeConf(conferenceDic,changePaper(paperDic,line)))
 #Reads and processes paper file
    with open(paperFilename, 'r') as PaperFile:    
        for line in PaperFile:
            temp = line.split(' ',1)
            temp2 = temp[0].split('#',1)
            if len(temp2) >1:
                tempkey = temp2[1].replace('>','')
                if paperDic.has_key(tempkey):
                    for prefix in paperDic[tempkey]:
                        output= prefix + '> ' + temp[1]
                        if output.find('<http://purl.org/ontology/bibo/status>') <0:
                            tempText = changePaper(paperDic, cleaner(output) )
                            text = tempText
                            #.replace('<http://www.w3.org/2002/07/owl#NamedIndividual>','<http://swrc.ontoware.org/ontology#Publication>') \
                            #.replace('<http://purl.org/ontology/bibo/Article>','<http://swrc.ontoware.org/ontology#InProceedings>') \
                            tmpFile.write(text) 

 #Reads and processes conference file
    with open(conferenceFilename, 'r') as confFile:    
        for line in confFile:
            tmpFile.write(line)
            
    tmpFile.close()

 # Replaces LREmap prefix with linghub   
    with open('tmp.nt', 'r') as TempFile:
        for line in TempFile:
           outFile.write(line.replace('http://www.resourcebook.eu/lremap/owl/lremap_ri/','http://linghub.lider-project.eu/lremap/')) 

    outFile.close()
    os.remove('tmp.nt')  

if __name__ == '__main__':

    paperFilename = 'data/lremap_paper.nt'
    submissionFilename = 'data/lremap_sub.nt'
    resourceFilename = 'data/lremap_ri.n3'
    conferenceFilename = 'data/lremap_conf.n3'
    outputFilename = 'LREmap2014.nt'
    
    main()