from pyht import Client
from pyht.client import TTSOptions, Language

class AudioGenUtil:
    def __init__(self, audio_client: Client, voice_url: str):
        self.audio_client = audio_client
        self.voice_url = voice_url

    def generate_audio(self, script: str, lang: Language):
        chunks : bytearray = bytearray()
        ttsOptions = TTSOptions(voice=self.voice_url, language=lang)
        for chunk in self.audio_client.tts(script, self.ttsOptions):
            chunks.extend(chunk)
        return chunks