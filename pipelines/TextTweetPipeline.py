from twikit import Client
from util.TextGenUtil import TextGenUtil

class TextTweetPipeline:
    def __init__(self, text_gen_util: TextGenUtil, tweet_client: Client):
        self.text_gen_util = text_gen_util
        self.tweet_client = tweet_client

    async def generate_text_tweet(self):
        text_content = self.text_gen_util.create_text_tweet_caption()
        self.tweet_client.create_tweet(text=text_content)