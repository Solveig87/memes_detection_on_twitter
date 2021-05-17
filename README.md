# Détection de mème sur Twitter

**Projet effectué dans le cadre d'un stage de M2 TAL au sein du laboratoire STIH à la Sorbonne**

**Auteur : Solveig PODER**

## Collecte des tweets avec la librairie Tweepy

Avant de lancer le script *extract_tweets_KW*, il faudra copier en local le fichier *.env.bak*, le renommer en *.env* et le compléter avec vos clés et tokens Twitter. Si vous n'en disposez pas, il suffit de créer un projet sur le portail développeurs de Twitter afin de les générer automatiquement.
Le script prend deux arguments :
- un fichier json comprenant la liste des recherches à effectuer sur Twitter (correspondant chacune à un mème recherché) avec pour chacune la date de la dernière collecte de tweets effectuée (par défaut *data/log_data/already_extracted.json*) : à faire précéder de ```-q```
- un fichier json comprenant la liste des id des tweets déjà collectés (par défaut *data/log_data/already_done_tweets.json*) : à faire précéder de ```-t```


## Filtrage des tweets collectés

Le script *detect_candidates.py* effectue deux filtrages successifs sur les tweets collectés via le script précédent :
- le premier filtrage associé à un mème les tweets qui possèdent un minimum de mots communs avec lui (à définir dans les paramètres)
- le second filtrage ne garde les tweets associés à un mème par le premier filtrage que si au moins l'un d'eux a une distance de Bray-Curtis inférieure à un certain seuil (défini dans les paramètres) : la distance est calculé entre des vecteurs de ngrams (dont la taille est également à définir dans les paramètres).

Les résultats sont conservés dans un fichier json ainsi que dans un fichier HTML pour la visualisation.

Le script prend six arguments :
- le fichier json comprenant les mèmes à rechercher (par défaut *data/seeds/memes_seed.json*) : à faire précéder de ```-s```
- le corpus de tweets à analyser (un fichier json ou un répertoire, par défaut *data/tweets_collectes/corpus_2021-05-10_0.json*) : à faire précéder de ```-d```
- l'intersection minimale (pourcentage de mots communs) pour qu'un tweet soit considéré comme associé à un mème (par défaut **0.66**) : à faire précéder de ```-i```
- distance de Bray-Curtis maximum entre un tweet et le mème auquel il est associé pour que les tweets associés à ce mème soient conservés dans les fichiers de résultats (par défaut **0.9**) : à faire précéder de ```-t```
- tailles minimale et maximale des ngrams pour les vecteurs à comparer (par défaut **5, 11**) : à faire précéder de ```-n```
- type de tokens pour la vectorisation (*char*, *char_wb* ou *word*, par défaut **char**) : à faire précéder de ```-a```


#### Organisarion du repo

Le répertoire **data** contient les sous-répertoires suivants :
- **log_data** contient les fichiers à passer en input au script de collecte ainsi qu'un fichier extract.log qui garde une trace de tous les lancements du script
- **tweets_collectes** contient les fichiers de sortie (au format json) du script de collecte, fichiers qui seront ensuite passés en entrée du script de filtrage
- **seeds** contient des fichiers comprenant une liste des mèmes que l'on passera en entrée du script de filtrage
- **final_output** contient les fichiers générés par le script de filtrage : un fichier html et un fichier json à chaque lancement du script
- un script, *create_query.py*, qui permet d'ajouter des recherches dans le fichier already_extracted.json à partir d'une nouvelle liste de mèmes

Le répertoire **modules** comprend le module *tools.py* contenant les fonctions appelées par les deux scripts principaux.

