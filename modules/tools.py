import json, re, glob 
import difflib
from scipy import spatial
from sklearn.feature_extraction.text import CountVectorizer
import codecs#utile sous windows
from difflib import SequenceMatcher
from datetime import datetime

def write_utf8(path, out, verbose =True, is_json = False):
  w = codecs.open(path,'w','utf-8')
  if is_json==False:
    w.write(out)
  else:
    w.write(json.dumps(out, indent=2, ensure_ascii=False))
  w.close()
  if verbose:
    print("  Output : '%s'"%path)

def decouper_mots(texte):
  mots = re.findall("[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ-]*", texte)
  return mots

def ouvrir(chemin, is_json=False):
  f = open(chemin)
  if is_json==True:
    D =json.load(f)
  else:
    D = f.read()
  f.close()
  return D

def write_file(chemin, data, is_json = False):
  w = open(chemin, "w")
  if is_json ==True:
    data = json.dumps(data, indent=2, ensure_ascii=False)
  w.write(data)
  w.close()

def tokeniser(content):
  W = content.lower().split()
  W = [x for x in W if len(x)>1]
  return W

def get_distances(liste, options):
  mini, maxi = [int(x) for x in re.split(",", options.n_grams)]
  V = CountVectorizer(ngram_range=(mini, maxi), analyzer = options.analyzer)
  return V.fit_transform(liste).toarray()

def check_distances(liste, X, seuil=0.9):
  meme = liste[0]
  candis = liste[1:]
  has_interest = False#au moins un truc intéressant, par défaut: encore rien
  res = []
  for cpt, x in enumerate(X[1:]):
    if meme.lower() in candis[cpt].lower(): #trouvé tel quel->pas intéressant
      continue
    dist = spatial.distance.braycurtis(X[0], x)
    res.append([dist, candis[cpt]])
    if dist<seuil:#au moins un truc proche
      has_interest = True
  return res, has_interest

def apply_seq_match(meme, seq, lower_case = True):
  if lower_case==True:
    meme = meme.lower()
    seq = seq.lower()
  S = SequenceMatcher(None, seq, meme)
  M = S.find_longest_match(0, len(seq), 0, len(meme))
  common = seq[M.a: M.a + M.size]
  offset_start = M.a
  seq = re.sub("\t|\r|\n", " ", seq)#pour affichage dans le tableur
  common = re.sub("\t|\r|\n", " ", common)#pour affichage dans le tableur
  try:
    start, end = re.split(common, seq)
  except:
    start = seq
    end =""
  return seq, common, start, end, offset_start 


def get_list_tweets(path_data):
  if ".json" in path_data:
    dic = ouvrir(path_data, True)
    liste_tweets = [d["tweet"] for d in dic]
  else:#by path
    path_data = "corpus"
    liste_tweets = [ouvrir(x) for x in glob.glob("corpus/*/*/*")]
  return liste_tweets

def display_res(res):
  print("-"*20)
  for cle, val in res.items():
    print(f"{cle} : '{val}'")
  print("-"*20)
  
def write_log(path, chaine):
  now = datetime.now()
  timestamp = now.isoformat()
  w = open(path, "a")
  #w.write(f"{timestamp} : {chaine}\n")
  w.write("%s : %s\n"%(timestamp, chaine))
  w.close()
