import pandas as pd
import glob
import os
from datetime import datetime
from country_data import country_names
import tweepy

def extract_top5(directory="charts"):
    today = datetime.now().strftime("%Y-%m-%d")
    kworb_url = "https://kworb.net/spotify/"

    csv_files = glob.glob(os.path.join(directory, f"*_dailytop50_{today}.csv"))
    if not csv_files:
        print(f"'{directory}' Chart file not found for today ({today}).")
        return None

    all_tweets = []

    for csv_file in csv_files:
        country_code = os.path.basename(csv_file).split('_')[0]
        display_name = country_names.get(country_code, country_code.upper())
        
        tweet_message = f"--- Spotify Today's Top 5 - {display_name} ---\n"
        rows_to_read = 5
        # Vietnam chart changed to Top 3 announcement due to X character limit
        if country_code == 'vn': 
            rows_to_read = 3
            tweet_message = f"--- Spotify Today's Top 3 - {display_name} ---\n" 

        try:
            df = pd.read_csv(csv_file, header=None, nrows=rows_to_read, encoding='utf-8-sig')

            if df.empty:
                tweet_message += "No data available."
            else:
                for index, row in df.iterrows():
                    rank = row[1]
                    title = row[2]
                    artist = row[3]
                    tweet_message += f"#{rank}: {title} {artist}\n"
 
            tweet_message += f"{kworb_url}\n"
            
            all_tweets.append(tweet_message)

        except Exception as e:
            print(f"An error occurred while loading the file '{csv_file}': {e}")
    
    return all_tweets

def post_tweets(tweet_messages):
    if not tweet_messages:
        print("No tweets to post.")
        return

    consumer_key = os.environ.get("TWITTER_API_KEY")
    consumer_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Twitter API credentials are not set in environment variables.")
        return

    try:
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
 
        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

        for message in tweet_messages:
            if len(message) > 280:
                print(f"Warning: Tweet message exceeds 280 characters ({len(message)}). Truncating.")
                message = message[:277] + "..." 
            
            print(f"Attempting to tweet:\n{message}")
            try:
                response = client.create_tweet(text=message)
                print(f"Successfully tweeted: {response.data['id']}")
            except tweepy.TweepyException as e:
                print(f"Error tweeting: {e}")
            
    except tweepy.TweepyException as e:
        print(f"Twitter API authentication error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during tweeting: {e}")

if __name__ == "__main__":
    tweets_to_post = extract_top5()
    if tweets_to_post:
        post_tweets(tweets_to_post)
