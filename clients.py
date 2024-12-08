from dotenv import load_dotenv, find_dotenv
import os
from mistralai import Mistral
from pyht import Client as PlayHtClient
from tweepy import Client as TweepyClient, OAuth2AppHandler, OAuth1UserHandler, API as TweepyV1API

load_dotenv(find_dotenv())

tweet_client = TweepyClient(bearer_token=os.getenv("BEARER_TOKEN_TWITTER"), 
                            consumer_key=os.getenv("API_KEY_TWITTER"), 
                            consumer_secret=os.getenv("API_SECRET_TWITTER"), 
                            access_token=os.getenv("ACCESS_TOKEN_TWITTER"), 
                            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET_TWITTER"))
auth = OAuth1UserHandler(
    os.getenv("API_KEY_TWITTER"), 
    os.getenv("API_SECRET_TWITTER"), 
    os.getenv("ACCESS_TOKEN_TWITTER"), 
    os.getenv("ACCESS_TOKEN_SECRET_TWITTER")
)

media_upload_client = TweepyV1API(auth)

llm_client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))

play_ht_client = PlayHtClient(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY"),
    auto_connect=False
)