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


def parse_response(response_json: str) -> List[HumePredictionResponse]:
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


def calculate_average_emotions(
    api_response: List[HumePredictionResponse],
) -> Dict[str, float]:
    total_emotions = defaultdict(float)
    emotion_counts = defaultdict(int)

    for prediction_response in api_response:
        for file_prediction in prediction_response.results.predictions:
            for (
                grouped_prediction
            ) in file_prediction.models.prosody.grouped_predictions:
                for prediction in grouped_prediction.predictions:
                    for emotion in prediction.emotions:
                        if (
                            emotion.name.lower() in POSITIVE_EMOTIONS
                            or emotion.name.lower() in NEGATIVE_EMOTIONS
                        ):
                            total_emotions[emotion.name] += emotion.score
                            emotion_counts[emotion.name] += 1

    average_emotions = {
        emotion: total_emotions[emotion] / emotion_counts[emotion]
        for emotion in total_emotions
    }

    max_avg_emotion = max(average_emotions.values(), default=1)
    normalized_emotions = {
        emotion: score / max_avg_emotion for emotion, score in average_emotions.items()
    }

    return normalized_emotions


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
