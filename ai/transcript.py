import requests
import json
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

HUMEAI_APIKEY = os.getenv("HUMEAI_APIKEY")
HUMEAI_BATCH_JOB_ENDPOINT = os.getenv("HUMEAI_BATCH_JOB_ENDPOINT")

# Debugging: Print the loaded environment variables
print(f'API Key: {HUMEAI_APIKEY}')
print(f'Batch Job Endpoint: {HUMEAI_BATCH_JOB_ENDPOINT}')

def start_inference_job(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            "json": json.dumps({
                "models": {
                    "prosody": {
                        "granularity": "utterance",
                        "identify_speakers": False
                    }
                },
                "notify": True
            })
        }
        
        response = requests.post(
            HUMEAI_BATCH_JOB_ENDPOINT,
            headers={
                'X-Hume-Api-Key': HUMEAI_APIKEY
            },
            files=files,
            data=data
        )
        response.raise_for_status()
        return response.json()['job_id']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an audio file for emotion analysis and transcript extraction.")
    parser.add_argument('-f', '--audio_file', type=str, required=True, help='Path to the audio file to be processed')
    args = parser.parse_args()

    audio_file_path = args.audio_file

    try:
        job_id = start_inference_job(audio_file_path)
        print(f'Batch job created with ID: {job_id}')
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e}')
        print(f'Response content: {e.response.content}')
