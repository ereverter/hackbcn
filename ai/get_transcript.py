# hume_analysis.py

import argparse
import json
import os
from collections import defaultdict
from typing import Dict, List

import requests
from dotenv import load_dotenv

from .domain import HumePredictionResponse

load_dotenv()

HUMEAI_APIKEY = os.getenv("HUMEAI_APIKEY")
HUMEAI_PREDICTION_ENDPOINT = "https://api.hume.ai/v0/batch/jobs/{job_id}/predictions"


def fetch_job_predictions(job_id: str, api_key: str) -> str:
    url = HUMEAI_PREDICTION_ENDPOINT.format(job_id=job_id)
    headers = {"X-Hume-Api-Key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_response(response_json: str):
    response_dict = json.loads(response_json)

    # def print_keys(d, level=0):
    #     if isinstance(d, dict):
    #         for key, value in d.items():
    #             print("  " * level + f"Level {level}: {key}")
    #             print_keys(value, level + 1)
    #     elif isinstance(d, list):
    #         for item in d:
    #             print_keys(item, level)

    return [HumePredictionResponse(**prediction) for prediction in response_dict]


def group_transcription(api_response: List[HumePredictionResponse]) -> str:
    transcriptions = []
    for prediction_response in api_response:
        for file_prediction in prediction_response.results.predictions:
            for (
                grouped_prediction
            ) in file_prediction.models.prosody.grouped_predictions:
                for prediction in grouped_prediction.predictions:
                    transcriptions.append(prediction.text)
    return " ".join(transcriptions)


def aggregate_emotions(
    api_response: List[HumePredictionResponse], interval: float
) -> Dict[float, Dict[str, float]]:
    emotion_aggregation = defaultdict(lambda: defaultdict(float))
    for prediction_response in api_response:
        for file_prediction in prediction_response.results.predictions:
            for (
                grouped_prediction
            ) in file_prediction.models.prosody.grouped_predictions:
                for prediction in grouped_prediction.predictions:
                    start_time = prediction.time.begin
                    interval_start = int(start_time // interval) * interval
                    for emotion in prediction.emotions:
                        emotion_aggregation[interval_start][
                            emotion.name
                        ] += emotion.score

    for interval_start, emotions in emotion_aggregation.items():
        total_score = sum(emotions.values())
        if total_score > 0:
            for emotion in emotions:
                emotions[emotion] /= total_score

    return dict(emotion_aggregation)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze job predictions from Hume AI."
    )
    parser.add_argument("job_id", type=str, help="The job ID to fetch predictions for")
    parser.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="Interval in seconds to aggregate emotions",
    )
    args = parser.parse_args()

    try:
        response_json = fetch_job_predictions(args.job_id, HUMEAI_APIKEY)
        api_response = parse_response(response_json)

        transcription_text = group_transcription(api_response)
        print("Transcription Text:")
        print(transcription_text)

        emotions_aggregated = aggregate_emotions(
            api_response, args.interval * 60
        )  # convert to seconds
        print("\nEmotions Aggregated:")
        for time, emotions in emotions_aggregated.items():
            print(f"Time {time/60} minutes:")
            for emotion, score in emotions.items():
                print(f"  {emotion}: {score:.2f}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response content: {e.response.content}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
