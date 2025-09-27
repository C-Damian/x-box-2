import os
import json
import tweepy
from dotenv import load_dotenv
import boto3

ssm = boto3.client("ssm")

def get_secret(param_name):
    response = ssm.get_parameter(
        Name=param_name,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]

# Load environment variables
load_dotenv()

client = tweepy.Client(
    bearer_token=get_secret(os.getenv("TWITTER_BEARER_TOKEN")),
    consumer_key=get_secret(os.getenv("TWITTER_API_KEY")),
    consumer_secret=get_secret(os.getenv("TWITTER_API_SECRET")),
    access_token=get_secret(os.getenv("TWITTER_ACCESS_TOKEN")),
    access_token_secret=get_secret(os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
)

def post_tweet(tweet_content: str) -> tuple:
    try:
        # Post the tweet
        response = client.create_tweet(text=tweet_content)

        # Convert Tweepy response to dict
        response_data = json.loads(json.dumps(response.data))

        tweet_id = response_data.get("id")
        print(f"Tweet posted successfully! Tweet ID: {tweet_id}")
        return True, tweet_id

    except Exception as e:
        print(f"Error posting tweet: {str(e)}")
        return False, None


'''
if __name__ == "__main__":
    test_tweet = "Hello from  X Bot! 🤖 #TechTip #Coding"
    success, tweet_id = post_tweet(test_tweet)
    if success:
        print(f"Test tweet posted with ID: {tweet_id}")
    else:
        print("Test tweet failed")
'''