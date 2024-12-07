from util.ContentIdeaGenerator import ContentIdeaGenerator
from util.AudioGenUtil import AudioGenUtil
from util.ImageGenUtil import ImageGenUtil
import replicate
from tweepy import Client, API
from pyht.client import Language
import os
import requests

class AnimatedImagePipeline:
    def __init__(self, audio_gen_util: AudioGenUtil, content_idea_generator: ContentIdeaGenerator, 
                 image_gen_util: ImageGenUtil, tweet_client: Client, media_upload_client: API):
        self.audio_gen_util = audio_gen_util
        self.content_idea_generator = content_idea_generator
        self.image_gen_util = image_gen_util
        self.tweet_client = tweet_client
        self.media_upload_client = media_upload_client
    
    def generate_animated_image(self, audio: bytearray, image_bytes):
        with open("assets/animated_image_img.png", "wb") as fi:
            fi.write(image_bytes.read())
        with open("assets/animated_image_audio.mp3", "wb") as fo:
            fo.write(audio)
        
        output = replicate.run(
            "cjwbw/sadtalker:a519cc0cfebaaeade068b23899165a11ec76aaa1d2b313d40d214f204ec957a3",
            input={
                "driven_audio": open("assets/animated_image_audio.mp3", "rb"),
                "source_image": open("assets/animated_image_img.png", "rb"),
                "use_enhancer": True,
                "preprocess": "full"
            }
        )

        os.remove("assets/animated_image_img.png")
        os.remove("assets/animated_image_audio.mp3")

        output_vid_url = output["output"]
        response = requests.get(output_vid_url)
        video_bytes = bytearray(response.content)
        return video_bytes

    def generate_animated_image_tweet(self, lang: Language):
        script = self.content_idea_generator.generate_for_audio()
        audio = self.audio_gen_util.generate_audio(script, lang)

        image_caption = self.content_idea_generator.generate_for_image()
        image = self.image_gen_util.generate_image_from_text_caption(image_caption)
        
        video = self.generate_animated_image(audio, image)
        video_id = self.media_upload_client.media_upload(video)

        self.tweet_client.create_tweet(media_ids=[video_id])
