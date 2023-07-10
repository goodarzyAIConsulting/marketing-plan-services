import gradio as gr

from function.ui_functions import (
    change_day_content_description_json,
    generate_content,
    display_weekly_marketing_plan,
)


def generate_content_ui():
    with gr.Blocks() as third_page:
        social_media = gr.Radio(
            choices=["Facebook", "Twitter", "Instagram", "LinkedIn"],
            label="social media",
        )

        number_of_week = gr.Number(
            label="Duration (in weeks)",
        )

        whole_week_program = gr.Dataframe(row_count=7, col_count=4)
        number_of_week.change(
            fn=display_weekly_marketing_plan,
            inputs=[social_media, number_of_week],
            outputs=whole_week_program,
        )

        # Define the list of days of the week
        days_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Create a dropdown component for the days of the week
        day_dropdown = gr.Dropdown(choices=days_of_week, label="Select a day")

        day_content_description = gr.JSON(label="JSON Output")

        business_description = gr.Textbox(
            label="Business Description"
        )  # Business description
        goals = gr.Textbox(label="Goals")
        target_audience = gr.Textbox(label="Target Audience", value="")
        content_specification = gr.Textbox(label="Content Specification", value="")

        model_name = gr.Radio(
            choices=["text-davinci-003", "gpt-3.5-turbo"], label="Model Name"
        )

        # generate_content_meta_btn = gr.Button("Generate")

        # content_meta_prompt = gr.Textbox(label="Content Meta Prompt")
        # content_meta = gr.JSON(label="Content Meta")
        # number_of_images = gr.Number(label="Number of images")

        txt_to_image_btn = gr.Button("Text to Image Generator")
        gallery = gr.Gallery(columns=4, rows=4)
        caption = gr.Textbox(label="caption")
        hashtag = gr.Textbox(label="hashtag")
        # content_meta = gr.JSON(label="Content Meta")

        social_media.change(
            fn=change_day_content_description_json,
            inputs=[social_media, day_dropdown, number_of_week],
            outputs=[business_description, goals, day_content_description],
        )
        # generate_content_meta_btn.click(generate_content, inputs=[day_content_description, business_description, social_media, goals ,target_audience,content_specification,model_name], outputs=[content_meta_prompt, content_meta])
        # generate_content_meta_btn.click(generate_content, inputs=[day_content_description, business_description, social_media, goals ,target_audience,content_specification,model_name], outputs=[content_meta_prompt, content_meta])

        # txt_to_image_btn.click(generate_image_text_to_image, inputs=[content_meta, number_of_images], outputs=[gallery, caption, hashtag])
        txt_to_image_btn.click(
            generate_content,
            inputs=[
                day_content_description,
                business_description,
                social_media,
                goals,
                target_audience,
                content_specification,
                model_name,
            ],
            outputs=[gallery, caption, hashtag],
        )

    return third_page
