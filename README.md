# Détection de mème sur Twitter

**Projet effectué dans le cadre d'un stage de M2 TAL au sein du laboratoire STIH à la Sorbonne**

**Auteur : Solveig PODER**

## Collecte des tweets avec la librairie Tweepy

Avant de lancer le script *extract_tweets_KW*, il faudra compléter le fichier *.env* avec vos clés et tokens Twitter. Si vous n'en disposez pas, il suffit de créer un projet sur le portail développeurs de Twitter afin de les générer automatiquement.
Le script prend deux arguments :
- un fichier json comprenant la liste des recherches à effectuer sur Twitter (correspondant chacune à un mème recherché) avec pour chacune la date de la dernière collecte de tweets effectuée : à faire précéder de ```-q```
- un fichier json comprenant la liste des id des tweets déjà collectés : à faire précéder de ```-t```


## Filtrage des tweets collectés

Le script *detect_candidates.py* effectue deux filtrages successifs sur les tweets collectés via le script précédent.


#### Organisarion du repo

Le répertoire **data** contient les sous-répertoires suivants :
- **log_data** contient les fichiers à passer en input au script de collecte ainsi qu'un fichier extract.log qui garde une trace de tous les lancements du script
- **tweets_collectes** contient les fichiers de sortie (au format json) du script de collecte, fichiers qui seront ensuite passés en entrée du script de filtrage
- **seeds** contient des fichiers comprenant une liste des mèmes que l'on passera en entrée du script de filtrage
- **final_output** contient les fichiers générés par le script de filtrage : un fichier html et un fichier json à chaque lancement du script

Le répertoire **modules** comprend le module *tools.py* contenant les fonctions appelées par les deux scripts principaux.

