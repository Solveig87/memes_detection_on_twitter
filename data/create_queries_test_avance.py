#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re
import spacy

# chargement du modèle spacy
nlp = spacy.load('fr_core_news_lg')

# Récupération du fichier input
parser = argparse.ArgumentParser(description = "fichier")
parser.add_argument("-v", "--verbose", help = "verbose mode", action = "store_true")
parser.add_argument("input_file", help = "path of input file")
args = parser.parse_args()

queries = {}

#on y ajoute les requêtes Twitter générées automatiquement à partir du nouveau fichier 'seed'
with open(args.input_file, encoding = "utf8") as memes:
    memes = json.load(memes)
    for meme in memes:
        query = re.sub("-", "", " ".join([token.text for token in nlp(meme.lower()) if not (token.is_punct or token.is_stop or token.is_space or token.pos_ == "ADJ" or token.text in ("x", "y"))]).strip())
        stopwords = re.sub(r"_+", "_", " ".join([token.text if token.is_stop or token.pos_ == "ADJ" else "_" for token in nlp(meme.lower())]))
        stopwords = " ".join(['"'+expr.strip()+ '"' for expr in stopwords.split("_") if len(expr.split())>2])
        stopwords = re.sub(r"([\'’]) ", r"\1", stopwords)
        if stopwords:
            query += " " + stopwords
        if len(query.split())<=1:
            query = " ".join([token.text for token in nlp(meme.lower()) if not (token.is_punct or token.is_space or token.text in ("x", "y"))]).strip()
            query = re.sub(r"([\'’]) ", r"\1", query)
            query = re.sub(" -", "-", query)
        queries[query] = ""
        

with open("log_data/already_extracted_test_avance.json", "w") as output:
    output.write(json.dumps(queries, ensure_ascii=False, indent=4))