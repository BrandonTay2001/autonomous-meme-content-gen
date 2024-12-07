from twikit import Client
from util import TextGenUtil

class TextTweetPipeline:
    def __init__(self, textGenUtil: TextGenUtil, tweetClient: Client):
        self.textGenUtil = textGenUtil
        self.tweetClient = tweetClient

    async def generateTextTweet(self):
        textContent = self.textGenUtil.createTextTweetCaption()
        self.tweetClient.create_tweet(text=textContent)