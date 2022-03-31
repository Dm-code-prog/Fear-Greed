
def twitter():
    import tweepy
    import numpy as np
    import pandas as pd
    import re
    import pickle
    from functions import clean_tweet
    emotions = {'sadness':0, 'joy':1, 'love':2, 'anger':3, 'fear':4, 'surprise':5}
    beerer_token = "AAAAAAAAAAAAAAAAAAAAAA8KaQEAAAAAj6Es%2B8NJqS5CbgwzAF0W2IFFyVQ%3DeXteJQzBU9DKELzFloA3xb6y9lAGclc1cv2sGZtzOyfFN0nBrJ"
    client = tweepy.Client(bearer_token=beerer_token)
    query = "bitcoin OR ethereum lang:en -is:retweet -has:media -has:links  -has:hashtags -is:reply is:verified -has:mentions"
    tweets = client.search_recent_tweets(query, max_results=100)
    count_vect = pickle.load(open('count_vect.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    texts = np.array([i['text'] for i in tweets.data])
    texts = [clean_tweet(i) for i in texts]
    data = count_vect.transform(texts)
    predictions = model.predict(data)
    fear = 0
    for i in predictions:
        if i == 'sadness' or i == 'fear' or i == 'anger':
            fear += 1
    print(f'Fear is {fear} out of {len(predictions)}')
    return fear


    