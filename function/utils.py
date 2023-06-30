import os
import json
import time
from pprint import pprint

import openai
from tqdm import tqdm


class PathManager(object):
    def __init__(self) -> None:
        config_path = "configs/path.json"

        with open(config_path, "r") as fin:
            paths = json.load(fin)

        self.__prompt_path = paths["prompt_path"]
        self.__save_path = paths["save_path"]

    @property
    def prompt_path(self):
        return self.__prompt_path

    @prompt_path.setter
    def prompt_path(self, prompt_path):
        self.__prompt_path = prompt_path

    @property
    def save_path(self):
        return self.__save_path

    @save_path.setter
    def save_path(self, save_path):
        self.__save_path = save_path


def initialize(api_key_input):
    openai.api_key = api_key_input


def generate_prompt(prompt_template: str, **kwargs) -> str:
    for key, value in kwargs.items():
        print(f"{key}: {value}")
        prompt_template = prompt_template.replace("{{{{{}}}}}".format(key), value)

    return prompt_template


def read_files(tempath):
    if not isinstance(tempath, str):
        file_path = tempath.name
    else:
        file_path = tempath

    if ".txt" in file_path:
        with open(file_path, "r") as file:
            content = file.read()

        return content

    if ".json" in file_path:
        with open(file_path, "r") as file:
            content = json.load(file)

        return content

    return None


def create_folder(folder_name: str, save_path: str = None):
    if save_path is None:
        save_path = os.getcwd()  # Set the default path for data

    save_path = os.path.join(save_path, folder_name)

    os.makedirs(save_path, exist_ok=True)  # Create folder to save

    return save_path


def save_output(json_object, folder_name: str, file_name: str, save_path: str = None):
    save_path = create_folder(folder_name, save_path)

    with open(os.path.join(save_path, f"{file_name}.json"), "w") as f:
        json.dump(json_object, f)


def generate_place_holders(json_obj):
    place_holders_list = []
    for social_media, plan in json_obj["social_media_platforms"].items():
        for key, value in plan.items():
            place_holders_list.append(
                {
                    "business_description": json_obj["business_description"],
                    "social_media_platforms": social_media,
                    "goals": " ".join(json_obj["goals"].values()),
                    "messaging": value["messaging"],
                    "promotion_tactic": value["promotion_tactics"],
                    "week_number": key,
                }
            )

    return place_holders_list


def generate_completion(prompt_template, model_name):
    """
    Generate a text completion based on the provided prompt and specified model name using the OpenAI API.

    Args:
        prompt_template (str): The prompt text to generate the completion from.
        model_name (str): The name of the model to use. Choose either 'text-davinci-003' or 'gpt-3.5-turbo'.

    Returns:
        tuple: A tuple containing the generated text output (str), a task class (str) and the total tokens used (int).

    Raises:
        ValueError: If an invalid model name is provided.

    Note:
        This function may raise a RateLimitError if the API rate limit is exceeded. If this happens, the function will automatically retry after a backoff period.
    """

    # Define the backoff function that waits for an increasing amount of time based on the retry count
    def backoff(retry_count):
        delay = 2**retry_count
        print(f"Rate limit exceeded. Retrying in {delay} seconds...")
        time.sleep(delay)

    # Define a dictionary of models and their respective parameters for text completion
    engines = {
        "text-davinci-003": {
            "create_fn": openai.Completion.create,
            "kwargs": {
                "engine": model_name,
                "prompt": prompt_template,
                # "max_tokens": 20,
                "temperature": 0,
                # "top_p": 1,
                # "frequency_penalty": 0,
                # "presence_penalty": 0,
            },
        },
        "gpt-3.5-turbo": {
            "create_fn": openai.ChatCompletion.create,
            "kwargs": {
                "model": model_name,
                "messages": [
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt_template},
                ],
                # "max_tokens": 10,
                # "n": 1,
                # "stop": None,
                "temperature": 0,
            },
        },
    }

    # Raise a ValueError if an invalid model name is provided
    if model_name not in engines:
        raise ValueError(
            "Invalid model name. Choose either 'text-davinci-003' or 'gpt-3.5-turbo'."
        )

    # Select the specified model
    engine = engines[model_name]
    retry_count = 0

    # Keep trying to generate the text completion until it succeeds or a non-retryable error occurs
    while True:
        try:
            # Use the OpenAI API to generate the text completion
            response = engine["create_fn"](**engine["kwargs"])

            # Return the generated text output, task class and total tokens used
            return response

        # If a rate limit error occurs, call the backoff function to wait before trying again
        except openai.error.RateLimitError:
            backoff(retry_count)
            retry_count += 1


def generate_marketing_plan_each_day(model_name, prompt_path=None, save_path=None):
    prompt_template = read_files(
        os.path.join(prompt_path, "content_generation_each_day_prompt.txt")
    )
    marketing_plan_json = read_files(
        os.path.join(save_path, "marketer_plan", "marketer_plan.json")
    )

    place_holders_list = generate_place_holders(marketing_plan_json)

    for place_holders in tqdm(place_holders_list, desc="generate the specific"):
        modified_prompt = generate_prompt(
            prompt_template=prompt_template, **place_holders
        )

        print(f"{modified_prompt = }")
        response = generate_completion(
            prompt_template=modified_prompt, model_name=model_name
        )

        json_output = response.choices[0].message.content
        try:
            json_obj = json.loads(json_output)
        except Exception:
            print(f"{Exception}")
            pprint(json_output)

        save_output(
            json_object=json_obj,
            folder_name=os.path.join(
                "marketer_plan", f"{place_holders['social_media_platforms']}"
            ),
            file_name=f"{place_holders['week_number']}_marketer_plan",
            save_path=save_path,
        )

    return prompt_template, json_output
