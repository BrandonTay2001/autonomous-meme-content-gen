import random
from dotenv import load_dotenv, find_dotenv
from pipelines import TextTweetPipeline, ImageTweetPipeline, AnimatedImagePipeline
from util.TextGenUtil import TextGenUtil
from util.ImageGenUtil import ImageGenUtil
from util.FaceSwapUtil import FaceSwapUtil
from util.AudioGenUtil import AudioGenUtil
from util.ContentIdeaGenerator import ContentIdeaGenerator
from pipelines.AnimatedImagePipeline import AnimatedImagePipeline
from pipelines.TextTweetPipeline import TextTweetPipeline
from pipelines.ImageTweetPipeline import ImageTweetPipeline
import json
import os
from mistralai import Mistral
from pyht import Client as PlayHtClient
from tweepy import Client as TweepyClient, OAuth1UserHandler, API as TweepyV1API
import time

load_dotenv(find_dotenv())
pipelines = ["text", "image", "animateImage"]

tweet_client = TweepyClient(bearer_token=os.getenv("BEARER_TOKEN_TWITTER"), 
                            consumer_key=os.getenv("API_KEY_TWITTER"), 
                            consumer_secret=os.getenv("API_SECRET_TWITTER"), 
                            access_token=os.getenv("ACCESS_TOKEN_TWITTER"), 
                            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET_TWITTER"))

auth = OAuth1UserHandler(
    consumer_key=os.getenv("API_KEY_TWITTER"),
    consumer_secret=os.getenv("API_SECRET_TWITTER"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET_TWITTER")
)

media_upload_client = TweepyV1API(auth)

llm_client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))
with open('config/character-bio.txt', 'r', encoding='utf-8') as f:
    character_bio = f.read()

play_ht_client = PlayHtClient(
    user_id=os.getenv("PLAY_HT_USER_ID"),
    api_key=os.getenv("PLAY_HT_API_KEY")
)

text_gen_util = TextGenUtil(llm_client, character_bio)
image_gen_util = ImageGenUtil(os.getenv("REPLICATE_LORA_MODEL"))
face_swap_util = FaceSwapUtil()
content_idea_generator = ContentIdeaGenerator(character_bio)
audio_gen_util = AudioGenUtil(play_ht_client, os.getenv("PLAY_HT_VOICE_URL"))

text_tweet_pipeline = TextTweetPipeline(text_gen_util, tweet_client)
image_tweet_pipeline = ImageTweetPipeline(image_gen_util, tweet_client, text_gen_util, content_idea_generator, media_upload_client)
animate_image_tweet_pipeline = AnimatedImagePipeline(audio_gen_util, content_idea_generator, 
                                                     image_gen_util, tweet_client, media_upload_client)

def useRandomPipeline():
    chosen_pipeline = random.choice(pipelines)
    if chosen_pipeline == "text":
        text_tweet_pipeline.generate_text_tweet()
    elif chosen_pipeline == "image":
        image_tweet_pipeline.generate_image_tweet()
    else:
        animate_image_tweet_pipeline.generate_animated_image_tweet()
    return

while True:
    useRandomPipeline()
    time.sleep(4 * 60 * 60)  # Sleep for 4 hours