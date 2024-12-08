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
from clients import llm_client, play_ht_client, tweet_client, media_upload_client
from pyht.client import Language
import os
import time

load_dotenv(find_dotenv())
pipelines = ["text", "image", "animateImage"]

with open('config/character-bio.txt', 'r', encoding='utf-8') as fb:
    character_bio = fb.read()
fb.close()
with open('config/image-prompt.txt', 'r', encoding='utf-8') as fip:
    image_prompt = fip.read()
fip.close()

text_gen_util = TextGenUtil(llm_client, character_bio)
image_gen_util = ImageGenUtil(os.getenv("REPLICATE_LORA_MODEL"), image_prompt)
face_swap_util = FaceSwapUtil()
content_idea_generator = ContentIdeaGenerator(character_bio, llm_client)
audio_gen_util = AudioGenUtil(play_ht_client, os.getenv("PLAY_HT_VOICE_URL"))

text_tweet_pipeline = TextTweetPipeline(text_gen_util, tweet_client)
image_tweet_pipeline = ImageTweetPipeline(image_gen_util, tweet_client, text_gen_util, content_idea_generator, media_upload_client)
animate_image_tweet_pipeline = AnimatedImagePipeline(audio_gen_util, content_idea_generator, 
                                                     image_gen_util, tweet_client, media_upload_client)

def useRandomPipeline():
    probabilities = [0.25, 0.50, 0.25]
    chosen_pipeline = random.choices(pipelines, probabilities)[0]
    print(f"Chosen pipeline: {chosen_pipeline}")
    if chosen_pipeline == "text":
        text_tweet_pipeline.generate_text_tweet()
    elif chosen_pipeline == "image":
        image_tweet_pipeline.generate_image_tweet()
    else:
        animate_image_tweet_pipeline.generate_animated_image_tweet(Language.ENGLISH)
    return

# while True:
#     try:
#         useRandomPipeline()
#     except Exception as e:
#         print(e)
#     time.sleep(5 * 60)

# while True:
#     useRandomPipeline()
#     time.sleep(1 * 60 * 60)  # Sleep for 1 hours