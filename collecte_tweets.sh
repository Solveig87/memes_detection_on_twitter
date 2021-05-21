#!/bin/bash

path1=$(python3 extract_tweets_KW.py -q data/log_data/already_extracted_basique.json -t data/log_data/already_done_tweets_basique.json)
path2=$(python3 extract_tweets_KW.py -q data/log_data/already_extracted_avance.json -t data/log_data/already_done_tweets_avance.json)

python3 compare_results.py $path1 $path2 data/seeds/memes_seed_fr.json data/log_data/already_extracted_basique.json data/log_data/already_extracted_avance.json

