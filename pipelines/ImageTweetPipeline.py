from util.ImageGenUtil import ImageGenUtil
from util.TextGenUtil import TextGenUtil
from util.ContentIdeaGenerator import ContentIdeaGenerator
from tweepy import Client, API

class ImageTweetPipeline:
    def __init__(self, image_gen_util: ImageGenUtil, tweet_client: Client, text_gen_util: TextGenUtil,
                 content_idea_generator: ContentIdeaGenerator, media_upload_client: API):
        self.image_gen_util = image_gen_util
        self.tweet_client = tweet_client
        self.text_gen_util = text_gen_util
        self.content_idea_generator = content_idea_generator
        self.media_upload_client = media_upload_client

    def generate_image_tweet(self) -> None:
        idea = self.content_idea_generator.generate_for_image()
        image = self.image_gen_util.generate_image_from_text_caption(idea)
        text_content = self.text_gen_util.create_accompanying_text_for_image_tweet(idea)
        image_id = self.media_upload_client.media_upload(image.read())
        self.tweet_client.create_tweet(text=text_content, media_ids=[image_id])
