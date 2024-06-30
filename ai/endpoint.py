import json
import os
import time
from typing import Any, Dict

import openai
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile

load_dotenv()

from .domain import TranscriptEvaluationRequest, TranscriptEvaluationResponse
from .evaluate import create_prompt, create_system_prompt
from .get_transcript import (
    aggregate_emotions,
    calculate_average_emotions,
    fetch_job_predictions,
    filter_emotions,
    group_transcription,
    group_transcription_by_time,
    parse_response,
)
from .process_audio import start_inference_job
from .process_video import extract_audio

app = FastAPI()


def save_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        buffer.write(file.file.read())
    return destination


@app.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    video_path = os.path.join(temp_dir, file.filename)
    audio_path = os.path.join(temp_dir, f"{os.path.splitext(file.filename)[0]}.wav")

    try:
        save_file(file, video_path)
        extract_audio(video_path, audio_path)
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    audio_path = save_file(file, f"temp/{file.filename}")

    try:
        # job_id = start_inference_job(audio_path)
        # return {"job_id": job_id}
        time.sleep(3)
        return {"job_id": "782b9a58-b09b-4d9b-9ead-952b7a2d85a6"}
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get("/fetch_predictions/{job_id}/{agg_time}")
async def fetch_predictions(job_id: str, agg_time: float):
    print(os.getenv("HUMEAI_APIKEY"))
    try:
        response_json = fetch_job_predictions(job_id, os.getenv("HUMEAI_APIKEY"))
        api_response = parse_response(response_json)

        transcription_text = group_transcription(api_response)

        grouped_transcription = group_transcription_by_time(api_response, agg_time)
        emotions_aggregated = aggregate_emotions(grouped_transcription)

        detailed_transcription = []
        for interval_start, texts_emotions in grouped_transcription.items():
            combined_text = " ".join(text for text, _ in texts_emotions)
            interval_emotions = emotions_aggregated[interval_start]
            detailed_transcription.append(
                (interval_start, combined_text, interval_emotions)
            )

        return {
            "transcription": transcription_text,
            "grouped_transcription": filter_emotions(detailed_transcription),
            "emotions_summary": calculate_average_emotions(api_response),
        }
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@app.post("/evaluate_transcript", response_model=TranscriptEvaluationResponse)
async def evaluate_transcript(request: TranscriptEvaluationRequest):
    try:
        # prompt = create_prompt(request.transcript, request.ground_truth)
        # client = openai.OpenAI()

        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": create_system_prompt()},
        #         {"role": "user", "content": prompt},
        #     ],
        # )

        # print(response)
        # feedback = response.choices[0].message.content
        response = {
            "feedback": '{\n    "errors": [\n        "In the transcript, at 30 seconds, the speaker deviates from the original plan by discussing the importance of drop bears, which was not part of the planned content for that section.",\n        "At 150 seconds in the transcript, the speaker introduces the term \'virus available and spatial analysis method\', which was not part of the original presentation.",\n        "The delivery lacks consistent pacing and some parts of the speech feel rushed, impacting clarity and audience engagement.",\n        "The emotional delivery is somewhat monotone and could benefit from more varied tones to emphasize key points and maintain audience interest."\n    ],\n    "recommendations": [\n        "Rehearse the presentation to ensure adherence to the planned content and avoid unnecessary tangents like discussing drop bears.",\n        "Work on pacing during the speech to allow for better clarity and comprehension of the complex scientific content.",\n        "Practice incorporating more varied emotional tones in delivery to enhance engagement and highlight the importance of specific results and findings."\n    ]\n}'
        }
        return TranscriptEvaluationResponse(feedback=response["feedback"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
