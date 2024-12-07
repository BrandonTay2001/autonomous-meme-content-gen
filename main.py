import asyncio
import random
from dotenv import load_dotenv, find_dotenv
from pipelines import TextTweetPipeline, ImageTweetPipeline, AnimatedImagePipeline
from twikit import Client
from util import TextGenUtil, ImageGenUtil, FaceSwapUtil, ContentIdeaGenerator
import json
import os
from mistralai import Mistral

load_dotenv(find_dotenv())
pipelines = ["text", "image", "animateImage"]

tweetClient = Client(language='en-us')
with open('config/cookies.json', 'r', encoding='utf-8') as f:
    tweetClient.set_cookies(json.load(f))

llmClient = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))
with open('config/character-bio.txt', 'r', encoding='utf-8') as f:
    characterBio = f.read()

textGenUtil = TextGenUtil(llmClient, characterBio)
imageGenUtil = ImageGenUtil(os.getenv("REPLICATE_LORA_MODEL"))
faceSwapUtil = FaceSwapUtil()
contentIdeaGenerator = ContentIdeaGenerator(characterBio)

textTweetPipeline = TextTweetPipeline(textGenUtil, tweetClient)
imageTweetPipeline = ImageTweetPipeline(imageGenUtil, tweetClient, textGenUtil, contentIdeaGenerator)
animateImageTweetPipeline = AnimatedImagePipeline()

def main():
    chosenPipeline = random.choice(pipelines)
    if chosenPipeline == "text":
        asyncio.run(textTweetPipeline.generateTextTweet())
    elif chosenPipeline == "image":
        asyncio.run(imageTweetPipeline.generateImageTweet())
    else:
        pass