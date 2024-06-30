import base64
import json
import os
from typing import Any, Dict, List

import openai
from dotenv import load_dotenv

from .config import ANALYSIS_INTERVAL_SECONDS

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def create_prompt(
    transcript: List[Any], ground_truth: str, body_language: str = None
) -> str:

    prompt = f"""
    Evaluate the following transcript against the provided ground truth:

    Transcript
    ---
    {transcript}

    Ground Truth
    ---
    {ground_truth}

    Optional[Body Language]
    {body_language}

    ### Remember
    Provide a json with a list of strings such that we can defien bullet points:
    - Specific timestamps where improvements can be made.
    - Parts of the speech where deviations from the original plan occurred.
    - General comments on the delivery and emotion.
    - Always comment on the body language.
    - PROVIDE VALID JSON!
    """
    return prompt


def create_system_prompt() -> str:
    return """
    You are an expert coach in public speaking with extensive experience in helping individuals improve their presentations. Your expertise encompasses various aspects of public speaking, including delivery, emotion, clarity, and adherence to the planned content. Your goal is to provide constructive feedback that helps people enhance their public speaking skills.

    When evaluating a transcript against the provided ground truth, you should focus on the following areas:

    1. **Specific Timestamps and Deviations from the Original Plan:** Identify precise moments in the transcript where improvements can be made. The should be pointed out only if the deviance from the plan is significant, otherwise it is okay.

    2. **General Comments on Delivery and Emotion:** Provide insights into the speaker's delivery given the provided emotions values. If body langauge analysis is also available, add more value to the answer with it given any issues.

    3. NO YAPPING

    Your feedback should be organized in a clear and understandable manner. The final response should be a JSON object containing two main keys:
    - "errors": A list of strings, each pointing out a specific error or area for improvement.
    - "recommendations": A list of strings, each offering a constructive suggestion to enhance the presentation.

    Example JSON response:
    {
        "errors": [
            "Forgot to talk about X at time Y",
        ],
        "recommendations": [
            "Practise more from the minute X to minute Y, where you feel less confident and prepared",
        ]
    }
    """


def create_body_language_prompt():
    return """
    You are an expert in public speeches and what body language conveys. Look at the image, and do something turbo simple, if the person has its hands in their pockets, point it out, otherwise say everything is fine. If there is no person in the image, say nothing.
    """


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_body_language_evaluation(frames_path: str, interval: int):
    client = openai.OpenAI()
    body_language = {}
    frame_files = sorted(
        [f for f in os.listdir(frames_path) if f.endswith(("png", "jpg", "jpeg"))]
    )
    for i, frame in enumerate(frame_files):
        timestamp = i * interval
        base64_image = encode_image(frames_path + frame)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": create_body_language_prompt()},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Briefly comment on the body language. One liner.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
        )

        body_language[timestamp] = response.choices[0].message.content

    return body_language


def evaluate(transcript, ground_truth, body_language_activated=True):
    body_language = None
    if body_language_activated:
        body_language = get_body_language_evaluation(
            "temp/", interval=ANALYSIS_INTERVAL_SECONDS
        )
    prompt = create_prompt(transcript, ground_truth, body_language)
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": create_system_prompt()},
            {"role": "user", "content": f"{prompt}"},
        ],
        response_format={"type": "json_object"},
    )

    feedback = response.choices[0].message.content
    return feedback
