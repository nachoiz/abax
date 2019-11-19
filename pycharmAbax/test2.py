#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tweepy as tw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import re


import nltk
from nltk.corpus import stopwords
import networkx

import warnings
warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")



###############################
###                         ###
###      Functions          ###
###                         ###
###############################


def read_token(filename):
	f = open(filename, "r")
	token_list = []
	for x in f:
		# Extract strings between single quotes
		sToken = re.findall(r"'(.*?)'", x, re.DOTALL)
		token_list.append(sToken)
	return token_list


def remove_url(txt):
	# Replaces URLs found in a text string with nothing
	# r means that the string is to be treated as a raw string
	# http matches literal characters
	# \S+ matches all non-whitespace characters (the end of the url)

	# Remove @username
	txt = re.sub("@[^\s]+","",txt)

	# Remove #hashtag
	txt = txt.replace("#", "")

	# Remove punctuation
	txt = re.sub(r"[^\w\s]", "",txt)

	# Remove http://link
	return " ".join(re.sub(r"http\S+", "", txt).split())


###############################
###                         ###
###      Main program       ###
###                         ###
###############################

## Abax Twitter tokens
abax_token_list = []
abax_token_list = read_token('/Users/Nacho/Documents/Ignacio/token.txt')

## Tokens
consumer_key = abax_token_list[1]
consumer_secret = abax_token_list[2]
access_token = abax_token_list[3]
access_token_secret = abax_token_list[4]

## Authentication OAuth
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)



search_term = "#vox -filter:retweets"

tweets = tw.Cursor(api.search,
		q=search_term,
		lang="es",
		since='2019-11-01').items(100)

all_tweets = [tweet.text for tweet in tweets]
all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]

# All tweets words in one list
words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

# -----------------------------------------------------------------------------
# Spanish prepositions
prep_es = ['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'hasta', 'hacia', 'para', 'por', 'segun', 'sin', 'so', 'sobre', 'tras']

conj_es = ['y', 'e', 'o', 'que', 'pero', 'sino', 'aunque']

# Determinantes
# Articulo
det_art_es = ['el', 'la', 'lo', 'los', 'las', 'al', 'del']

# Demostrativos
det_dem_es = ['este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'aquel', 'aquella', 'aquellos', 'aquellas']

# Posesivosf
det_pos_es = ['mi', 'su', 'tu']

# Indefinidos
det_ind_es = ['un', 'uno', 'una', 'unos', 'unas']

# Pronombres personales
pron_es = ['yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros', 'ellos', 'ellas', 'me', 'te', 'le', 'se', 'nos', 'os', 'les', 'se']

otras_es = ['tal']

# -------------------------------------------------------------------------------

# Remove recurrent wording
words_set = prep_es + conj_es + det_art_es + det_dem_es + det_pos_es + det_ind_es + pron_es + otras_es

flat_list_words = []
for i in range(0, len(words_in_tweet)):
	for elem in words_in_tweet[i]:
		flat_list_words.append(elem)

for word in list(flat_list_words):
	if word in words_set:
		flat_list_words.remove(word)
	

# List of all words across tweets
#all_words_no_urls = list(itertools.chain(*flat_list_words))

# Create counter
counts_no_urls = collections.Counter(flat_list_words)
#print(counts_no_urls.most_common(15))

clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
				columns = ['words', 'count'])

print(clean_tweets_no_urls.head(10))




