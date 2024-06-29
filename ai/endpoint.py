import json
import os
from typing import Any, Dict

import requests
from fastapi import FastAPI, File, HTTPException, UploadFile

from .get_transcript import (
    aggregate_emotions,
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
    audio_path = save_file(file, f"uploads/{file.filename}")

    try:
        job_id = start_inference_job(audio_path)
        return {"job_id": job_id}
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get("/fetch_predictions/{job_id}")
async def fetch_predictions(job_id: str, agg_time: float):
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
        }
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
