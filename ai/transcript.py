import requests
import json
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

HUMEAI_APIKEY = os.getenv["HUMEAI_APIKEY"]
HUMEAI_UPLOAD_ENDPOINT = os.getenv["HUMEAI_UPLOAD_ENDPOINT"]
HUMEAI_BATCH_JOB_ENDPOINT = os.getenv["HUMEAI_BATCH_JOB_ENDPOINT"]

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            HUMEAI_UPLOAD_ENDPOINT,
            headers={'Authorization': f'Bearer {HUMEAI_APIKEY}'},
            files={'file': f}
        )
        response.raise_for_status()
        return response.json()['file_id']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an audio file for emotion analysis and transcript extraction.")
    parser.add_argument('-f', '--audio_file', type=str, help='Path to the audio file to be processed')
    args = parser.parse_args()

    video_file_path = args.video_file
    video_file_id = upload_file(video_file_path)

    batch_job_payload = {
        "models": {
            "prosody": {
                "granularity": "utterance",
                "identify_speakers": False
            }
        },
        "registry_files": [video_file_id],
    }

    response = requests.post(
        HUMEAI_BATCH_JOB_ENDPOINT,
        headers={'Authorization': f'Bearer {HUMEAI_APIKEY}', 'Content-Type': 'application/json'},
        data=json.dumps(batch_job_payload)
    )

    response.raise_for_status()
    job_id = response.json()['job_id']
    print(f'Batch job created with ID: {job_id}')
