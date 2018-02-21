from collections import Counter

import tweepy
from django.conf import settings

MAX_TWEETS = 200

im1url = ''

def tweets_analysis(tweets):
    tweet_timeline = []
    tweet_hashtags = ""
    for tweet in tweets:
        tweet_timeline.append(str(tweet.created_at.date()))
        for hash in tweet.entities['hashtags']:
            tweet_hashtags += " " + hash['text'].lower()
    tweet_timeline = list(sorted(Counter(tweet_timeline).items(), reverse=True, key=lambda x: x[0]))
    tweet_hashtags = list(sorted(Counter(tweet_hashtags.split(' ')).items(), reverse=True, key=lambda x: x[1]))
    tweet_timeline = {'date': [str(x[0]) for x in tweet_timeline], 'count': [x[1] for x in tweet_timeline]}
    tweet_hashtags = {'tag': [str(x[0]) for x in tweet_hashtags], 'count': [x[1] for x in tweet_hashtags]}
    return {'hashtags_count': tweet_hashtags, 'timeline': tweet_timeline, }


class TwitterApi(object):
    def __init__(self):

        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_secret = settings.ACCESS_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def get_user_profile(self, username):
        return self.api.get_user(screen_name=username)

    def get_user_tweets(self, username, number_of_tweets=1):
        alltweets = []
        kwargs = {'screen_name': username, 'include_rts': 0,
                  'count': number_of_tweets if number_of_tweets < MAX_TWEETS else MAX_TWEETS}
        length = 0
        while length < number_of_tweets:
            new_tweets = self.api.user_timeline(**kwargs)
            if not new_tweets:
                break
            alltweets.extend(new_tweets)
            length = len(alltweets)
            diff = number_of_tweets - length
            oldest = alltweets[-1].id - 1
            kwargs.update({'max_id': oldest, 'count': MAX_TWEETS if diff > MAX_TWEETS else diff})
        return alltweets

    def get_user_im_urls(self, alltweets):
        # kwargs = {'count': number_of_tweets if number_of_tweets < MAX_TWEETS else MAX_TWEETS}
        # i=0
        outtweets = [] #initialize master list to hold our ready tweets
        for tweet in alltweets:
        #not all tweets will have media url, so lets skip them
            try:
                print tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                     #we dont want to have any entries without the media_url so lets do nothing
                pass
            else:
                # i = i+1
                    #got media_url - means add it to the output
                    #outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
                outtweets.append([tweet.entities['media'][0]['media_url']])

        # kwargs.update({'count': i})
        return outtweets

    def get_user_im_score(self, imurls):
        # kwargs = {'count': number_of_tweets if number_of_tweets < MAX_TWEETS else MAX_TWEETS}
        
        #for im in imurls:
        #     try:
        #         print jlsm.io/ed/eval.py?img_url= im
        score = .75
        # kwargs.update({'count': i})
        return score

    def get_user_im_url_count(self, imurls):
        outtweets = [] #initialize master list to hold our ready tweets
        i=0
        for im in imurls:
        #not all tweets will have media url, so lets skip them
            if i==0:
                im1url = im
            #got media_url - means add it to the output
                    #outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
            i = i+1
            # outtweets.append([tweet.entities['media'][0]['media_url']])

        return i

    def get_user_im_url1(self, imurls):
        return im1url

