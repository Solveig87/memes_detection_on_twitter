#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re

def bold_KW(meme, tweet):
    for keyword in re.sub('"', "", meme).split():
        tweet = " ".join([word if word.lower() != keyword and word.lower() not in (keyword+",", keyword+".", keyword+"?", keyword+"!", keyword+"\"", "\""+keyword) else "**"+word+"**" for word in tweet.split()])
    return tweet

# Récupération des fichiers à comparer
parser = argparse.ArgumentParser(description = "fichier")
parser.add_argument("-v", "--verbose", help = "verbose mode", action = "store_true")
parser.add_argument("input_file1", help = "path of input file 1")
parser.add_argument("input_file2", help = "path of input file 2")
parser.add_argument("memes_list", help = "path of the list of memes")
parser.add_argument("queries1", help = "path of the list of queries 1")
parser.add_argument("queries2", help = "path of the list of queries 2")
args = parser.parse_args()

#on récupère d'abord les données des fichiers qu'on souhaite comparer
with open(args.input_file1, encoding = "utf8") as f:
    tweets1 = json.load(f)
with open(args.input_file2, encoding = "utf8") as f:
    tweets2 = json.load(f)
with open(args.memes_list, encoding = "utf8") as f:
    memes = json.load(f)
with open(args.queries1, encoding = "utf8") as f:
    queries1 = json.load(f)
with open(args.queries2, encoding = "utf8") as f:
    queries2 = json.load(f)

liste_id_tweets1 = [tweet['metadata']['id'] for tweet in tweets1]
liste_id_tweets2 = [tweet['metadata']['id'] for tweet in tweets2]

#on fait les listes des tweets communs et des tweets propres à chaque fichier
queries = []
for i in range(len(memes)):
    queries.append([memes[i], list(queries1.keys())[i], list(queries2.keys())[i]])
#print(queries)
common_tweets = {}
only_tweets1 = {}
only_tweets2 = {}
for query in queries:
    common_tweets[query[0]] = set([tweet['tweet'] for tweet in tweets1 if tweet['metadata']['id'] in liste_id_tweets2 and tweet['query'] == query[1]])
    only_tweets1[query[0]] = set([tweet['tweet'] for tweet in tweets1 if tweet['metadata']['id'] not in liste_id_tweets2 and tweet['query'] == query[1]])
    only_tweets2[query[0]] = set([tweet['tweet'] for tweet in tweets2 if tweet['metadata']['id'] not in liste_id_tweets1 and tweet['query'] == query[2]])

#on écrit les résultats dans un fichier
filename = args.input_file1.split("/")[-1].split(".")[0] + "_VS_" + args.input_file2.split("/")[-1].split(".")[0] + ".md"
with open(filename, "w", encoding = "utf8") as output:
    for query in queries:
        output.write("\n\t# "+query[0]+"\n\n")
        output.write("## Tweets communs\n")
        for tweet in common_tweets[query[0]]:
            output.write(bold_KW(query[1], re.sub("\n", " ", tweet)))
            output.write("\n")
        output.write("\n## Tweets propres au premier fichier\n")
        for tweet in only_tweets1[query[0]]:
            output.write(bold_KW(query[1], re.sub("\n", " ", tweet)))
            output.write("\n")
        output.write("\n## Tweets propres au second fichier\n")
        for tweet in only_tweets2[query[0]]:
            output.write(bold_KW(query[2], re.sub("\n", " ", tweet)))
            output.write("\n")