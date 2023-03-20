from diffusers import StableDiffusionPipeline
import torch
# print(torch.cuda.is_available())

device = torch.device("cpu")
model_id = "nitrosocke/nitro-diffusion"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "archer arcane style magical princess with golden hair"
image = pipe(prompt).images[0]

image.save("./magical_princess.png")