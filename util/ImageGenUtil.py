import replicate

class ImageGenUtil:
    def __init__(self, model: str):
        self.model = model
        self.prompt = ""

    def generate_image_from_text_caption(self, caption: str):
        output = replicate.run(
            self.model,
            input={
                "model": "dev",
                "prompt": f"{caption} {self.prompt}",
                "lora_scale": 1,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "guidance_scale": 3.5,
                "output_quality": 90,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        )
        return output[0]
    
    def generate_image_from_image_prompt(self):
        pass
