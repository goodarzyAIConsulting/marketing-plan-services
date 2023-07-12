import os
import json
import gradio as gr
import pandas as pd
from pprint import pprint  # should be deleteds

from function.utils import (
    save_output,
    read_files,
    generate_completion,
    generate_prompt,
    generate_marketing_plan_each_day,
    PathManager,
)

from model.stable_diffusion import generate_image_text_to_image


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

    pprint(response)

    if model_name == "gpt-3.5-turbo":
        json_output = response.choices[0].message.content
    elif model_name == "text-davinci-003":
        json_output = response.choices[0].text.strip()
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

    if isinstance(social_media_platforms, list):
        social_media_platforms = social_media_platforms[0]

    marketing_weekly_plan_json = read_files(
        os.path.join(
            path_manager.save_path,
            "marketer_plan",
            f"{social_media_platforms}",
            f"week_1_marketer_plan.json",
        )
    )

    df = pd.DataFrame(marketing_weekly_plan_json["week_days"]).T
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "week_days"}, inplace=True)

    return df


def generate_content(
    day_content_description,
    business_description,
    social_media,
    goals,
    target_audience,
    content_specification,
    model_name,
    progress=gr.Progress(track_tqdm=True),
):
    path_manager = PathManager()

    prompt_template = read_files(
        os.path.join(
            path_manager.prompt_path, "content_generation_caption_hashtagh_image.txt"
        )
    )

    place_holder = {
        "business_description": business_description,
        "social_media_platforms": social_media,
        "goals": goals,
        "content_description": day_content_description["content_description"],
        "content_type": day_content_description["content_type"],
        "target_audience": target_audience,
        "content_specification": content_specification,
    }

    prompt_template = generate_prompt(prompt_template, **place_holder)

    response = generate_completion(
        prompt_template=prompt_template, model_name=model_name
    )

    json_output = response.choices[0].message.content
    marketing_plan_json = json.loads(json_output)

    img = generate_image_text_to_image(marketing_plan_json)

    # print("Everything has been ran perfectly")
    # pprint(marketing_plan_json)
    # print(f"{img}")

    return (
        gr.Gallery.update(value=img),
        marketing_plan_json["caption"],
        "#".join(marketing_plan_json["hashtags"]),
    )


def change_day_content_description_json(social_media, day_dropdown, number_of_week):
    if isinstance(number_of_week, float):
        number_of_week = int(number_of_week)

    path_manager = PathManager()

    marketing_plan_json = read_files(
        os.path.join(
            path_manager.save_path,
            "marketer_plan",
            f"{social_media}",
            f"week_{number_of_week}_marketer_plan.json",
        )
    )

    return (
        gr.Textbox.update(
            label="Business Description",
            value=marketing_plan_json["business_description"],
        ),
        gr.Textbox.update(
            label="Goals", value="\n".join(marketing_plan_json["goals"].values())
        ),
        gr.JSON.update(
            label="JSON Output", value=marketing_plan_json["week_days"][day_dropdown]
        ),
    )


def display_weekly_marketing_plan(social_media, number_of_week):
    if isinstance(number_of_week, float):
        number_of_week = int(number_of_week)
    path_manager = PathManager()

    marketing_weekly_plan_json = read_files(
        os.path.join(
            path_manager.save_path,
            "marketer_plan",
            f"{social_media}",
            f"week_{number_of_week}_marketer_plan.json",
        )
    )

    df = pd.DataFrame(marketing_weekly_plan_json["week_days"]).T
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={"index": "week_days"}, inplace=True)

    return gr.DataFrame.update(value=df)
