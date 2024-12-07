import asyncio
import random
from dotenv import load_dotenv, find_dotenv
from pipelines import TextTweetPipeline, ImageTweetPipeline, AnimatedImagePipeline
from twikit import Client
from util.TextGenUtil import TextGenUtil
from util.ImageGenUtil import ImageGenUtil
from util.FaceSwapUtil import FaceSwapUtil
from util.ContentIdeaGenerator import ContentIdeaGenerator
from pipelines.AnimatedImagePipeline import AnimatedImagePipeline
from pipelines.TextTweetPipeline import TextTweetPipeline
from pipelines.ImageTweetPipeline import ImageTweetPipeline
import json
import os
from mistralai import Mistral

load_dotenv(find_dotenv())
pipelines = ["text", "image", "animateImage"]

tweet_client = Client(language='en-us')
with open('config/cookies.json', 'r', encoding='utf-8') as f:
    tweet_client.set_cookies(json.load(f))

llm_client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))
with open('config/character-bio.txt', 'r', encoding='utf-8') as f:
    characterBio = f.read()

text_gen_util = TextGenUtil(llm_client, characterBio)
image_gen_util = ImageGenUtil(os.getenv("REPLICATE_LORA_MODEL"))
face_swap_util = FaceSwapUtil()
content_idea_generator = ContentIdeaGenerator(characterBio)

text_tweet_pipeline = TextTweetPipeline(text_gen_util, tweet_client)
image_tweet_pipeline = ImageTweetPipeline(image_gen_util, tweet_client, text_gen_util, content_idea_generator)
animate_image_tweet_pipeline = AnimatedImagePipeline()

def main():
    chosen_pipeline = random.choice(pipelines)
    if chosen_pipeline == "text":
        asyncio.run(text_tweet_pipeline.generate_text_tweet())
    elif chosen_pipeline == "image":
        asyncio.run(image_tweet_pipeline.generate_image_tweet())
    else:
        asyncio.run(animate_image_tweet_pipeline.generate_animated_image_tweet())