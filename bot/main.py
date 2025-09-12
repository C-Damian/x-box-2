import random
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from ai_tweet_generator import generate_tip
from twitter_client import post_tweet
from mangum import Mangum
import os

categories = {
        1: "Python",
        2: "JavaScript", 
        3: "DevOps",
        4: "Git",
        5: "Performance",
        6: "Security",
        7: "APIs"
    }

def todays_category():
  weekday = datetime.now(timezone.utc).weekday() + 1
  return categories.get(weekday, "Python")

def create_tweet_content(category: str) -> str:
  tip = generate_tip(category)
  return f"{tip['title']}\n\n{tip['content']}\n\n{tip['code_example']}\n\n{tip['hashtags']}"

# Determine today's category and generate the tweet content
category = todays_category()
tweet_content = create_tweet_content(category)

# Post the tweet and handle errors
try:
  success, tweet_id = post_tweet(tweet_content)
  if success:
    print(f"Tweet added to dynamoDB: {tweet_id}")
  else:
    print(f"Error posting tweet")
except Exception as e:
  print(f"Unexpected error: {str(e)}")


# main.py handler for AWS Lambda
def handler(event, context):
    print("Lambda triggered")
    # Post the tweet and handle errors
    try:
      success, tweet_id = post_tweet(tweet_content)
      if success:
        print(f"Tweet added to dynamoDB: {tweet_id}")
      else:
        print(f"Error posting tweet")
    except Exception as e:
      print(f"Unexpected error: {str(e)}")
      return {"statusCode": 200, "body": "Success"}

print(tweet_content)
print(success)