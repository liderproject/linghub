import nltk
from nltk.stem import *
import csv
import sys

def matchExpressions(expression1, expression2, mode):
	expression1 = preprocess(expression1, mode)
	expression2 = preprocess(expression2, mode)
	return (expression1 in expression2)


def preprocess(inputExpression, mode):
	if (mode == 'stringMatching'):
		return basicCleanup(inputExpression) 
	elif (mode == "stemmingPorter"):
		return stemmingPorter(inputExpression) 
	elif (mode == "stemmingSnowball"):
		return stemmingSnowball(inputExpression) 


def basicCleanup(inputExpression):
	return inputExpression.strip().lower().replace("/"," ").replace(","," ")

def stemmingPorter(inputExpression):
	inputExpression = basicCleanup(inputExpression)
	tokens = nltk.word_tokenize(inputExpression)
	stemmer = PorterStemmer()
	
	f = lambda x : stemmer.stem(x)
	results = map(f, tokens)
	
	return " ".join(results)

def stemmingSnowball(inputExpression):
	inputExpression = basicCleanup(inputExpression)
	tokens = nltk.word_tokenize(inputExpression)
	stemmer = SnowballStemmer("english", ignore_stopwords=True)

	f = lambda x : stemmer.stem(x)
	results = map(f, tokens)
	
	return " ".join(results)

linghubPrefix = "http://linghub.lider-project.eu/lremap/"
metasharePrefix = "http://purl.org/ms-lod/MetaShare.ttl#"
resourceUseMetashare = "{}{}".format(metasharePrefix, "useNLPSpecific")

metashareUsagesFile = "../metashare/META-SHARE-usages.csv"

mode = "stemmingPorter"
count = 0

metashareUsages = {}
with open(metashareUsagesFile, 'rU') as refFile:
	refReader = csv.reader(refFile, delimiter=',')
	for refRow in refReader:
		metashareUsages[refRow[1]] = refRow[0] # refRow[0] - URIfied META-SHARE usage, refRow[1] - title-like META-SHARE usage

for line in sys.stdin:
	line = line.strip()
	print line
	if "<http://www.resourcebook.eu/lremap/owl/lremap_resource.owl#Resourceuse>" in line:
		resourceID = line.split(" ", 1)[0]
		resourceUsage = line.split('"')[1]
		
		if resourceUsage == "":
			continue
		matches = []
		for mu in metashareUsages:
			if matchExpressions(mu, resourceUsage, mode):
				matches.append(metashareUsages[mu])
		if matches != []:
			count = count + 1
			for m in matches:
				print '{} <{}> <{}{}> .'.format(resourceID, resourceUseMetashare, metasharePrefix, m)
