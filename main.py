import argparse
from typing import Dict, Any
import openai

from function.utils import PathManager, initialize
from ui.generate_overall_plan import generate_overall_plan_ui


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api_key", type=str, default="test_project")

    return parser.parse_args()


def run(api_key: str):
    initialize(api_key)

    marketin_plan_main_page = generate_overall_plan_ui()

    return marketin_plan_main_page


def main(opts: Dict[str, Any]):
    api_key = opts["api_key"]
    tabbed_interface = run(api_key)

    return tabbed_interface


if __name__ == "__main__":
    opts = vars(parse_args())
    interface = main(opts)

    interface.queue().launch(debug=True, share=True)
