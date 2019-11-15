import os
import tweepy as tw
import pandas as pd

consumer_key = 'zUbiKqvr8AS6ns8MZlu88D84N'
consumer_secret = '5mKwxXG8NKhjtpC3iEJU0hIIopOz374c9XhcI0TqZ5k7XRQ0vb'
access_token = '1194185301243105280-2hmAEwkSbYzDtHk5SWL8PGKSGvZJHx'
access_token_secret = 'sAd1lsC3qhaRj4GRMEJl86GoI316RDDDyrQ5ZRPgasXYp'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True)

# Post a tweet
#api.update_status("Hello World! First Test.")

# Define the search term and the date_since date as variables
search_words = "#clasico"
date_since = "2019-11-13"

new_search = search_words + " -filter:retweets"

# Collect tweets
tweets = tw.Cursor(api.search,
		q = new_search,
		lang="es",
		since = date_since).items(5)

# Collect a list of tweets
all_tweets = [tweet.text for tweet in tweets]
print(all_tweets[:2])

# User locations
user_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]
#print(user_locs)

tweet_text = pd.DataFrame(data = user_locs,
			columns = ['user', "location"])

print(tweet_text)
