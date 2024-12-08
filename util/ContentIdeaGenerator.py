from mistralai import Mistral

class ContentIdeaGenerator:
    def __init__(self, character_bio: str, llm_client: Mistral):
        self.character_bio = character_bio
        self.llm_client = llm_client

    def generate_for_image(self) -> str:
        caption = self.llm_client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": f"Characte bio: {self.character_bio}\nYou are an image caption generator bot. You are tasked with generating a caption for an image, usually this will be in the form of the character doing some action or describing how the character looks while doing that action. Also describe the surroundings of the character if any, Example: '[Character] sitting on a table, eating cake while staring at a crowd'. Captions generated should be consistent with the character bio given, so actions taken by the character and the setting of the image must be consistent with the character."
                }, 
                {
                    "role": "user",
                    "content": "Create an image caption! Keep it short and simple."
                }
            ]
        )
        return caption.choices[0].message.content
    
    def generate_for_audio(self) -> str:
        script = self.llm_client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "system",
                    "content": f"Characte bio: {self.character_bio}\nYou are a bot that generates audio scripts - put yourself in the shoes of the character whose bio has been provided. Audio scripts should be consistent with what the character would say. Keep responses to less than 4 sentences, and do not return the response with quotation marks."
                }, 
                {
                    "role": "user",
                    "content": "Generate an audio script! Remember to stay consistent with the character."
                }
            ]
        )
        return script.choices[0].message.content
    
# Usage
'''
test_generator = ContentIdeaGenerator("Zhong Xina is an alter ego of John Cena that is patriotic toward the Chinese Communist Party (CCP). He will often say things like 'glory to the CCP', or engage in conversations praising the CCP to an unrealistic standard. He is also heavily in-tune with Chinese propaganda, so he despises everything Western and instead praises the Chinese counterpart. He deems anything from Western ideals as 'Western propaganda' and immediately discredits them.", Mistral(api_key="qv8ZYjIfE8U0pblto6HVPI9OqIJLfwsk"))
print(test_generator.generate_for_audio())
'''