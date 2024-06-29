# hume_analysis.py

import argparse
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

import requests
from dotenv import load_dotenv

from .config import NEGATIVE_EMOTIONS, POSITIVE_EMOTIONS
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


def group_transcription_by_time(
    api_response: List[HumePredictionResponse], interval: float
) -> Dict[float, List[Tuple[str, Dict[str, float]]]]:
    transcript_aggregation = defaultdict(list)
    for prediction_response in api_response:
        for file_prediction in prediction_response.results.predictions:
            for (
                grouped_prediction
            ) in file_prediction.models.prosody.grouped_predictions:
                for prediction in grouped_prediction.predictions:
                    start_time = prediction.time.begin
                    interval_start = int(start_time // interval) * interval
                    emotions = {
                        emotion.name: emotion.score for emotion in prediction.emotions
                    }
                    transcript_aggregation[interval_start].append(
                        (prediction.text, emotions)
                    )
    return dict(transcript_aggregation)


def aggregate_emotions(
    grouped_transcript: Dict[float, List[Tuple[str, Dict[str, float]]]]
) -> Dict[float, Dict[str, float]]:
    emotion_aggregation = {}
    for interval_start, texts_emotions in grouped_transcript.items():
        aggregated_emotions = defaultdict(float)
        for text, emotions in texts_emotions:
            for emotion, score in emotions.items():
                aggregated_emotions[emotion] += score
        max_score = max(aggregated_emotions.values(), default=1)
        if max_score > 0:
            for emotion in aggregated_emotions:
                aggregated_emotions[emotion] /= max_score
        emotion_aggregation[interval_start] = dict(aggregated_emotions)
    return emotion_aggregation


def filter_emotions(
    grouped_transcription: List[Tuple[float, str, Dict[str, float]]]
) -> List[Tuple[float, str, Dict[str, float]]]:
    filtered_transcription = []
    for interval_start, combined_text, emotions in grouped_transcription:
        filtered_emotions = {
            emotion: score
            for emotion, score in emotions.items()
            if emotion.lower() in POSITIVE_EMOTIONS
            or emotion.lower() in NEGATIVE_EMOTIONS
        }
        filtered_transcription.append(
            (interval_start, combined_text, filtered_emotions)
        )
    return filtered_transcription


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
