import gradio as gr

from function import generate_marketing_plan


def generate_overall_plan_ui(prompt_path: str = None, save_path: str = None):
    inputs = [
        gr.Textbox(
            label="Business Description", value="I am a tattoo artist"
        ),  # Business description
        gr.CheckboxGroup(
            choices=["Facebook", "Twitter", "Instagram", "LinkedIn"],
            label="Social Media Platforms",
        ),  # Social Media selection
        gr.Number(
            label="Duration (in weeks)",
        ),  # Number of weeks
        gr.Textbox(label="Goals", value="increase follower, gain customer"),  # Goals
        gr.Radio(
            choices=["text-davinci-003", "gpt-3.5-turbo"], label="Model Name"
        ),  # Select the
        prompt_path,
        save_path,
    ]

    outputs = [gr.Textbox(label="Template Prompt"), gr.JSON(label="JSON Output")]

    return gr.Interface(
        fn=generate_marketing_plan,
        # inputs=[api_key_input, model_name_input, business_description_input, social_media_platforms_input, duration_input, goals_input],
        inputs=inputs,
        outputs=outputs,
        title="Marketing Plan Generator",
        description="Generate a marketing plan based on your input.",
        theme="default",
    )
