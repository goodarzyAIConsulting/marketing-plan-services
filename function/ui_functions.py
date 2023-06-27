import os
import json
import gradio as gr

from .utils import (
    save_output,
    read_files,
    generate_completion,
    generate_prompt,
    generate_marketing_plan_each_day,
)


def generate_marketing_plan(
    business_description,
    social_media_platforms,
    duration,
    goals,
    model_name,
    prompt_path=None,
    save_path=None
    progress=gr.Progress(track_tqdm=True),
):
    if isinstance(duration, float):
        duration = int(duration)

    prompt_template = read_files(
        os.path.join(prompt_path, "content_generation_prompt.txt")
    )

    place_holder_value = {
        "business_description": business_description,
        "social_media_platforms": ",".join(social_media_platforms),
        "duration": str(duration),
        "goals": goals,
    }

    prompt_template = generate_prompt(prompt_template, **place_holder_value)

    response = generate_completion(
        prompt_template=prompt_template, model_name=model_name
    )

    json_output = response.choices[0].message.content
    marketing_plan_json = json.loads(json_output)

    save_output(
        json_object=marketing_plan_json,
        folder_name="marketer_plan",
        file_name="marketer_plan",
    )

    prompt_template, marketing_plan_json = generate_marketing_plan_each_day(model_name, prompt_path, save_path)

    return prompt_template, marketing_plan_json
