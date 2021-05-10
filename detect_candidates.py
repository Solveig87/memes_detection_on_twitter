import json, sys, re, glob 
import difflib, math
from scipy import spatial
from difflib import SequenceMatcher
import xlsxwriter
import random
from modules.tools import *

def get_args():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-s", "--name_seed", dest="name_seed",
		  default="data/seeds/memes_seed.json",
                  help="name_seed", metavar="NAMESEED")
  parser.add_option("-d", "--path_data", dest="path_data",
		  default="data/tweets_collectes/corpus_2021-05-10_0.json",
                  help="Can be a json_file (see README) or a directory", 
                  metavar="PATH_DATA")
  parser.add_option("-v", "--verbose",
                   action="store_true", dest="verbose", default=False,
                   help="print status messages to stdout")
  parser.add_option("-i", "--inter_ratio",
                   dest="inter_ratio", default=0.66, type = "float",
                   help="Words intersection threshold")
  parser.add_option("-t", "--threshold",
                   dest="threshold", default=0.9, type = "float",
                   help="Similarity threshold")
  parser.add_option("-n", "--n_grams",
                   dest="n_grams", default="5,11",
                   help="n_gram min and max (min,max)")
  parser.add_option("-a", "--analyzer",
                   dest="analyzer", default="char",
                   help="Token type for vectorization")
  (options, args) = parser.parse_args()
  L = ["char", "char_wb", "word"]
  if options.analyzer not in L:
    print("Unknown value for analyzer, (must be one of '%s')"%"' or '".join(L))
    print("Switching back to default : 'char'")
    options.analyzer = "char"
  return options

def analyse(dic_dist, name_seed, o):
  out = "" # pour la visu HTML
  dic_res = {} # pour la sortie au format json
  for meme, candis in dic_dist.items():
    done = []#No doubloons
    X = get_distances([meme]+candis, o) # mini = n_mini, maxi = n_maxi)
    res, has_interest = check_distances([meme]+candis, X, seuil = o.threshold)
    if has_interest ==True:
      dic_res.setdefault(meme, [])
      out+=f"<h1>{meme}</h1>\n<table>\n"#tableau pour un même
      for dist, seq in sorted(res):
        if seq in done:
          continue
        done.append(seq)
        dist = round(dist, 6)
        seq, common, start, end, offset_start = apply_seq_match(meme, seq)
        res = {"texte":seq,"distance":dist, "common_seg":common}
        dic_res[meme].append(res)
        if options.verbose==True:
          display_res(res)
        if len(common)>1:
          seq =  re.sub(common, f"<strong>{common}</strong>", seq)
        out+=f"<tr><td>{dist}</td><td>{seq}</td></tr>\n"
      out+="</table>\n"
  return out, dic_res

print("Usage  :\n  python detect_candidates.py -s [SEED_LIST] -d [TWEET_LIST]")
print("Example:\n  python detect_candidates.py -s memes_seed.json -d data_json/merge.json")

options = get_args()

name_seed = options.name_seed
liste_memes = ouvrir(name_seed, True)

path_data = options.path_data
liste_tweets = get_list_tweets(path_data)

#separer stockage candidats et application distances
#provisoire :

words_memes = [tuple(tokeniser(x)) for x in liste_memes]
set_words_memes = [set(x) for x in words_memes]

name_out_base = "data/final_output/"+re.sub("/", "__", f"{name_seed}-VS-{path_data}")


#### First Filtering ####
dic_dist = {}
for content in liste_tweets:
  w_candidat = tuple(tokeniser(content))
  set_w = set(w_candidat)
  for cpt, set_m in enumerate(set_words_memes):
    Inter = set_m.intersection(set_w)
    if len(Inter)>len(set_m)*options.inter_ratio:#intersection ratio
      dic_dist.setdefault(liste_memes[cpt], set())
      dic_dist[liste_memes[cpt]].add(content)

dic_dist = {x: list(y) for x, y in dic_dist.items()}#for serialization

print("NB examples with intersection : %i"%len(dic_dist))

if len(dic_dist)>0:
  res_html, res_json = analyse(dic_dist, name_out_base, options)
  write_utf8(f"{name_out_base}_candidates.json", res_json, is_json=True)
  write_utf8(f"{name_out_base}_vizu.html", res_html)

