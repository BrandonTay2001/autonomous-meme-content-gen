from mistralai import Mistral

class TextGenUtil:
    def __init__(self, llmClient: Mistral, characterBio: str):
        self.llmClient = llmClient
        self.characterBio = characterBio

    def createTextTweetCaption(self):
        tweet = self.llmClient.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": "You are a tweet bot that personifies a specific character. You are tasked with creating a tweet that is consistent with the character's personality. The character bio is: " + self.characterBio
                }, 
                {
                    "role": "user",
                    "content": "Create a tweet that is consistent with the character's personality. Just return the tweet on its own. Do not use hashtags or emojis in tweets and keep tweets to under 3 sentences long."
                }
            ]
        )
        return tweet.choices[0].message.content
    
    def createAccompanyingTextForImageTweet(self, imageCaption: str):
        caption = self.llmClient.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": "some system prompt"
                }, 
                {
                    "role": "user",
                    "content": f"Create an accompanying text for this! {imageCaption}"
                }
            ]
        )
        return caption.choices[0].message.content
    
