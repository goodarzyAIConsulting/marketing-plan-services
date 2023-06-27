import os
import json
import gradio as gr

from .utils import (
    save_output,
    read_files,
    generate_completion,
    generate_prompt,
    generate_marketing_plan_each_day,
    PathManager,
)


def generate_marketing_plan(
    business_description,
    social_media_platforms,
    duration,
    goals,
    model_name,
    progress=gr.Progress(track_tqdm=True),
):
    if isinstance(duration, float):
        duration = int(duration)

    path_manager = PathManager()

    prompt_template = read_files(
        os.path.join(path_manager.prompt_path, "content_generation_prompt.txt")
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
        save_path=path_manager.save_path,
    )

    prompt_template, marketing_plan_json = generate_marketing_plan_each_day(
        model_name, path_manager.prompt_path, path_manager.save_path
    )

    return prompt_template, marketing_plan_json
