from mistralai import Mistral

class ContentIdeaGenerator:
    def __init__(self, character_bio: str, llm_client: Mistral):
        self.character_bio = character_bio
        self.llm_client = llm_client

    def generate_for_image(self):
        # should return a caption for an image, eg: "{Character} sitting on a chair eating a sandwich"
        pass
    
    def generate_for_audio(self):
        # should return a script for an audio, eg: "Hello, how are you doing today?"
        pass