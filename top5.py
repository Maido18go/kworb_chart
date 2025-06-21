import pandas as pd
import glob
import os
from datetime import datetime
from country_data import country_names
import tweepy # 追加

def extract_top5(directory="charts"):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 検索する日付形式を調整 (kworb.pyの出力と合わせる)
    # kworb.pyで datetime.now().strftime("%Y-%m-%d") を使っている場合、そのままでOK
    # もしYYYYMMDD形式なら %Y%m%d に修正
    # 今回はkworb.pyと統一されているのでそのまま

    # Search files
    csv_files = glob.glob(os.path.join(directory, f"*_dailytop50_{today}.csv"))
    if not csv_files:
        print(f"'{directory}' Chart file not found for today ({today}).") # エラーメッセージを修正
        return None # 変更: ツイートがないことを示すためNoneを返す

    all_tweets = [] # 各国のツイートを格納するリスト

    for csv_file in csv_files:
        country_code = os.path.basename(csv_file).split('_')[0]
        display_name = country_names.get(country_code, country_code.upper()) # 国コードが見つからない場合、大文字の国コードを使用

        tweet_message = f"--- Spotify Today's Top 5 - {display_name} ---\n"
        
        try:
            df = pd.read_csv(csv_file, header=None, nrows=5, encoding='utf-8-sig')

            if df.empty:
                tweet_message += "No data available."
            else:
                for index, row in df.iterrows():
                    # 順位、曲名、アーティスト名のみを取得
                    # row[0] は日付 (不要)、row[1]は順位、row[2]はタイトル、row[3]はアーティスト
                    # kworb.pyの出力がrow[0]=日付, row[1]=順位, row[2]=タイトル, row[3]=アーティストの場合
                    rank = row[1]
                    title = row[2]
                    artist = row[3]
                    tweet_message += f"#{rank}: {title} {artist}\n"
            
            all_tweets.append(tweet_message) # ツイートメッセージを追加

        except Exception as e:
            print(f"An error occurred while loading the file '{csv_file}': {e}")
            # エラーが発生した場合は、その国のツイートは生成しないか、エラーメッセージをツイートに含めることも可能
            # all_tweets.append(f"Error processing {display_name} chart: {e}") 
    
    return all_tweets # 変更: 全てのツイートを返す

def post_tweets(tweet_messages):
    if not tweet_messages:
        print("No tweets to post.")
        return

    # 環境変数から認証情報を取得
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
        api = tweepy.API(auth)
        
        # Twitter API v2 Clientの準備 (tweepy 4.x以降)
        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

        for message in tweet_messages:
            if len(message) > 280: # Twitterの文字数制限 (旧140→現280)
                message = message[:277] + "..." # 長すぎる場合は切り詰める
            
            print(f"Attempting to tweet:\n{message}")
            try:
                # ツイートを投稿
                # Tweepy v4以降ではclient.create_tweet()を使用
                response = client.create_tweet(text=message)
                print(f"Successfully tweeted: {response.data['id']}")
            except tweepy.TweepyException as e:
                print(f"Error tweeting: {e}")
                # 特定のエラーコード（例: 重複ツイート）に対するハンドリングも可能
            
    except tweepy.TweepyException as e:
        print(f"Twitter API authentication error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during tweeting: {e}")

if __name__ == "__main__":
    # make sure charts directory exists (for local testing)
    # os.makedirs("charts", exist_ok=True) 

    # kworb.pyを先に実行してCSVファイルがchartsディレクトリに存在することを前提とする
    # GitHub Actionsではkworb.pyが先に実行されるため、これで問題ない

    tweets_to_post = extract_top5()
    if tweets_to_post:
        post_tweets(tweets_to_post)
