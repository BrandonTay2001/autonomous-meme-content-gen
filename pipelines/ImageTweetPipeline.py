from util import ImageGenUtil, TextGenUtil, ContentIdeaGenerator
from twikit import Client

class ImageTweetPipeline:
    def __init__(self, imageGenUtil: ImageGenUtil, tweetClient: Client, textGenUtil: TextGenUtil,
                 contentIdeaGenerator: ContentIdeaGenerator):
        self.imageGenUtil = imageGenUtil
        self.tweetClient = tweetClient
        self.textGenUtil = textGenUtil
        self.contentIdeaGenerator = contentIdeaGenerator

    async def generateImageTweet(self):
        idea = self.contentIdeaGenerator.generateForImage()
        image = self.imageGenUtil.generateImage(idea)
        textContent = self.textGenUtil.createAccompanyingTextForImageTweet(idea)
        image_id = await self.tweetClient.upload_media(image)
        await self.tweetClient.create_tweet(text=textContent, media_ids=[image_id])
