from pyht import Client
from pyht.client import TTSOptions, Language

class AudioGenUtil:
    def __init__(self, audio_client: Client, voice_url: str):
        self.audio_client = audio_client
        self.voice_url = voice_url

    def generate_audio(self, script: str, lang: Language) -> bytearray:
        chunks : bytearray = bytearray()
        ttsOptions = TTSOptions(voice=self.voice_url, language=lang)
        for chunk in self.audio_client.tts(script, ttsOptions):
            chunks.extend(chunk)
        self.audio_client.close()
        return chunks

# Usage
'''
testUtil = AudioGenUtil(Client(user_id="user_id", api_key="api_key"), 
                        "s3://voice-cloning-zero-shot/a59cb96d-bba8-4e24-81f2-e60b888a0275/charlottenarrativesaad/manifest.json")
audio = testUtil.generate_audio("Hello, this is a test", Language.ENGLISH)
# write to file
with open("audio.mp3", "wb") as f:
    f.write(audio)
'''