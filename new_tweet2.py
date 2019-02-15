#!"C:\Users\shruti\Anaconda3\python.exe"
# -*- coding: utf-8 -*-

import tweepy
import csv
import json
import datetime
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

    def get_all_tweets(screen_name):

        # Twitter allows access to only 3240 tweets via this method

        # Authorization and initialization

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

        # initialization of a list to hold all Tweets

        all_the_tweets = []

        # We will get the tweets with multiple requests of 200 tweets eac
        today=datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        new_tweets=api.user_timeline(screen_name=screen_name,since_id=yesterday)

        				               # saving the most recent tweets

        #outtweets = [tweet["text"] for tweet in new_tweets]
        
        natural_language_understanding = NaturalLanguageUnderstandingV1(
                    version='2018-11-16',
                        username='025eedb4-219b-4022-9986-26df9dcb995a',
                        password='nZu8gsGmwWAW',
                        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
                            )

        #outtweets=[tweet["text"] for tweet in new_tweets]

        outtweets=list()

        for tweet in new_tweets:
            if tweet["lang"]=='en':
                outtweets.append(tweet["text"])
        
        i=0
        sad=joy=fear=disg=ang=0
        while(i!=len(outtweets)):

            response = natural_language_understanding.analyze(text=outtweets[i],
                      features=Features(entities=EntitiesOptions( emotion=True, sentiment=True,limit=2),keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))).get_result()
                                              
            print(json.dumps(response, indent=2))
           # length=len(response["keywords"])
            #print(length)
            j=0
            
            while(j<len(response["keywords"])):
                temp1=response["keywords"][j]["emotion"]
                m=0
                while(m<len(temp1)):
                    sad=sad+temp1["sadness"]
                    joy=joy+temp1["joy"]
                    fear=fear+temp1["fear"]
                    disg=disg+temp1["disgust"]
                    ang=ang+temp1["anger"]
                    m=m+1
            

                j=j+1
            
            i=i+1

        print("sadness=",sad," joy=",joy," fear=",fear," disgust=",disg," anger=",ang)
        result=max(sad,joy,fear,disg,ang)
        print("prominent sentiment=",result)




        
        

get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))
