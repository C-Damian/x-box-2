import random
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from tweet_generator import generate_tip
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

print(generate_tip(todays_category()).get("title"))
