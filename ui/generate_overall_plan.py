import gradio as gr

from function import generate_marketing_plan
from function.ui_functions import display_weekly_marketing_plan


def generate_overall_plan_ui(prompt_path: str = None, save_path: str = None):
    with gr.Blocks() as first_page:
        business_description = gr.Textbox(
            label="Business Description", value="I am a tattoo artist"
        )

        social_media = gr.CheckboxGroup(
            choices=["Facebook", "Twitter", "Instagram", "LinkedIn"],
            label="Social Media Platforms",
        )

        week_duration = gr.Number(
            label="Duration (in weeks)",
        )

        goals = gr.Textbox(label="Goals", value="increase follower, gain customer")

        model = gr.Radio(
            choices=["text-davinci-003", "gpt-3.5-turbo"], label="Model Name"
        )

        plan_generator_btn = gr.Button("Plan Generator")

        number_of_week = gr.Number(label="Number of Week", value=1)

        whole_week_program = gr.Dataframe(row_count=7, col_count=4)

        plan_generator_btn.click(
            generate_marketing_plan,
            inputs=[business_description, social_media, week_duration, goals, model],
            outputs=[whole_week_program],
        )

        number_of_week.change(
            fn=display_weekly_marketing_plan,
            inputs=[social_media, number_of_week],
            outputs=whole_week_program,
        )

    return first_page
