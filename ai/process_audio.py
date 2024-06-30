import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

HUMEAI_APIKEY = os.getenv("HUMEAI_APIKEY")
HUMEAI_BATCH_JOB_ENDPOINT = os.getenv("HUMEAI_BATCH_JOB_ENDPOINT")


def start_inference_job(file_path: str) -> str:
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "json": json.dumps(
                {
                    "models": {
                        "prosody": {
                            "granularity": "utterance",
                            "identify_speakers": False,
                        }
                    },
                    "notify": True,
                }
            )
        }

        response = requests.post(
            HUMEAI_BATCH_JOB_ENDPOINT,
            headers={"X-Hume-Api-Key": HUMEAI_APIKEY},
            files=files,
            data=data,
        )
        response.raise_for_status()
        return response.json()["job_id"]
