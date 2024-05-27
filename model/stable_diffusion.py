import sys

sys.path.insert(0, "/content/stable-diffusion-pytorch")
print(f"{sys.path = }")

from stable_diffusion_pytorch import model_loader
from stable_diffusion_pytorch import pipeline


def generate_image_text_to_image(prompt_json, num_pic=1):
    if isinstance(num_pic, float):
        num_pic = int(num_pic)

    prompt = prompt_json["content_design_detail"]
    prompts = [prompt]

    uncond_prompt = ""
    uncond_prompts = [uncond_prompt] if uncond_prompt else None

    upload_input_image = False
    input_images = None
    # if upload_input_image:
    #     from PIL import Image
    #     from google.colab import files

    #     print("Upload an input image:")
    #     path = list(files.upload().keys())[0]
    #     input_images = [Image.open(path)]

    strength = 0.8

    do_cfg = True
    cfg_scale = 7.5
    height = 512
    width = 512
    sampler = "k_lms"
    n_inference_steps = 50

    use_seed = False  # @param { type: "boolean" }
    if use_seed:
        seed = 42  # @param { type: "integer" }
    else:
        seed = None

    models = model_loader.preload_models("cuda")

    img = pipeline.generate(
        prompts=prompts,
        uncond_prompts=uncond_prompts,
        input_images=input_images,
        strength=strength,
        do_cfg=do_cfg,
        cfg_scale=cfg_scale,
        height=height,
        width=width,
        sampler=sampler,
        n_inference_steps=n_inference_steps,
        seed=seed,
        models=models,
        device="cuda",
        idle_device="cpu",
    )

    return img
