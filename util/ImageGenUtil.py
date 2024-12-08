import replicate
from typing import Iterator

class ImageGenUtil:
    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt

    def generate_image_from_text_caption(self, caption: str) -> Iterator[bytes]:
        output = replicate.run(
            self.model,
            input={
                "model": "dev",
                "prompt": f"{self.prompt}\n\n{caption}",
                "lora_scale": 1,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "guidance_scale": 3.5,
                "output_quality": 90,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28,
                "disable_safety_checker": True
            }
        )
        return output[0]
    
    def generate_image_from_image_prompt(self):
        pass