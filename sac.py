import os
import tweepy

def tweet_message():
    message = "The Official Southeast Asia Charts has announced a new chart!\nhttps://www.officialseacharts.com/weeklychart"
    
    consumer_key = os.environ.get("TWITTER_API_KEY")
    consumer_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Twitter API credentials are not set in environment variables.")
        return

    try:
        # OAuth 1.0a 認証
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        
        # Twitter API v2 Clientの準備
        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

        print(f"Attempting to tweet:\n{message}")
        response = client.create_tweet(text=message)
        print(f"Successfully tweeted: {response.data['id']}")

    except tweepy.TweepyException as e:
        print(f"Error tweeting: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    tweet_message()
