import sys, re
from modules.tools import *
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import json
import os
from dotenv import load_dotenv
load_dotenv()

"""Connexion à l'API Twitter"""
auth = OAuthHandler(os.getenv('KEY'), os.getenv('SECRET_KEY'))
auth.set_access_token(os.getenv('TOKEN'), os.getenv('SECRET_TOKEN'))
auth_api = API(auth)

"""Récupération des arguments"""
def get_args():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-q", "--queries", dest="queries",
		  default="data/log_data/already_extracted.json",
                  help="queries", metavar="QUERIES")
  parser.add_option("-t", "--tweets_id", dest="tweets_id",
		  default="data/log_data/already_done_tweets.json",
                  help="list of tweets already collected", 
                  metavar="TWEETS_ID")
  (options, args) = parser.parse_args()
  return options

"""Lecture des fichiers en input"""
options = get_args()
dic_extracted = ouvrir(options.queries, is_json = True)
liste_KW = sorted([[date_last, Q] for Q, date_last in dic_extracted.items()])
already_done = ouvrir(options.tweets_id, is_json=True)


"""Récupération de nouveaux tweets"""
today = date.today()
date_str = today.strftime("%Y-%m-%d")

L = []
cpt, cpt_error = 0, 0
twitter_error = False

write_log("data/log_data/extract.log", "----START----")
msg = "Already Done (I) :", len(already_done)
print(msg)
write_log("data/log_data/extract.log", msg)

for date_last, Q in liste_KW:
  print(date_last, Q)
  #write_log("data/log_data/extract.log", f"{date_last}:{Q}")
  write_log("data/log_data/extract.log", "%s:%s"%(date_last, Q))
  try:
    for tweet in Cursor(auth_api.search, q=Q, rpp=100, result_type="recent", include_entities=True, lang="fr", tweet_mode='extended').items():
      name = tweet.user.screen_name
      date = tweet.created_at.isoformat()[:10]
      ID = tweet._json["id_str"]
      if ID in already_done:
        #print(f"->Already done : {ID}")
        print("->Already done : %s"%ID)
        break
      else:
        already_done.append(ID)
      if 'retweeted_status' in dir(tweet):
        txt=tweet.retweeted_status.full_text
      else:
        txt=tweet.full_text
      L.append({"date":date, "user":name, "tweet":txt, "metadata":tweet._json, "query":Q})
      cpt+=1
      if cpt%100==0:
        print("  ",txt)
        write_log("data/log_data/extract.log", re.sub("\n", "", txt))
        print("  ",cpt)
        #twitter_error = True
  except tweepy.TweepError as e:
      print(e)
      write_log("data/log_data/extract.log", str(e))
      cpt_error+=1
      if "429" in str(e): #too many requests
        twitter_error=True
        break
  print(cpt)
  if twitter_error==True:
    break
  dic_extracted[Q]=date_str

print("Already Done(II):", len(already_done))

dic_extracted[Q]=date_str

"""Mise à jour des inputs"""
write_file("data/log_data/already_extracted.json", dic_extracted, is_json = True)
write_file("data/log_data/already_done_tweets.json", json.dumps(already_done))

msg =  "got %i tweets"%len(L)
write_log("data/log_data/extract.log", msg)
print(msg)
print(cpt_error, "errors")

"""Création d'un nouveau fichier de data"""
import os
for i in range(10):
  path_out = "data/tweets_collectes/corpus_%s_%i.json"%(date_str, i)
  if os.path.exists(path_out)==False:
    break
print(path_out)
write_log("data/log_data/extract.log", path_out)
write_log("data/log_data/extract.log", "==== END ====")
write_file(path_out, L, is_json = True)
