from mistralai import Mistral

class TextGenUtil:
    def __init__(self, llm_client: Mistral, character_bio: str):
        self.llm_client = llm_client
        self.character_bio = character_bio

    def create_text_tweet_caption(self):
        tweet = self.llm_client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": "You are a tweet bot that personifies a specific character. You are tasked with creating a tweet that is consistent with the character's personality. The character bio is: " + self.character_bio
                }, 
                {
                    "role": "user",
                    "content": "Create a tweet that is consistent with the character's personality. Just return the tweet on its own. Do not use hashtags or emojis in tweets and keep tweets to under 3 sentences long."
                }
            ]
        )
        return tweet.choices[0].message.content
    
    def create_accompanying_text_for_image_tweet(self, image_caption: str):
        caption = self.llm_client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": "some system prompt"
                }, 
                {
                    "role": "user",
                    "content": f"Create an accompanying text for this! {image_caption}"
                }
            ]
        )
        return caption.choices[0].message.content
    
