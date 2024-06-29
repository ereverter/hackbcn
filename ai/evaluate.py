import os
from typing import Dict, List

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI()


class Emotion(BaseModel):
    name: str
    score: float


class TimeInterval(BaseModel):
    begin: float
    end: float


class TranscriptChunk(BaseModel):
    text: str
    time: TimeInterval
    emotions: List[Emotion]


class TranscriptEvaluationRequest(BaseModel):
    transcript: List[TranscriptChunk]
    ground_truth: List[TranscriptChunk]


class TranscriptEvaluationResponse(BaseModel):
    feedback: str


def create_prompt(
    transcript: List[TranscriptChunk], ground_truth: List[TranscriptChunk]
) -> str:
    transcript_text = "\n".join(
        [f"{chunk.time.begin}-{chunk.time.end}: {chunk.text}" for chunk in transcript]
    )
    ground_truth_text = "\n".join(
        [f"{chunk.time.begin}-{chunk.time.end}: {chunk.text}" for chunk in ground_truth]
    )

    prompt = f"""
    Evaluate the following transcript against the provided ground truth:

    Transcript:
    {transcript_text}

    Ground Truth:
    {ground_truth_text}

    Provide detailed feedback on the presentation, highlighting:
    - Specific timestamps where improvements can be made.
    - Parts of the speech where deviations from the original plan occurred.
    - General comments on the delivery and emotion.
    Organize the feedback in a clear and understandable manner.
    """
    return prompt


@app.post("/evaluate_transcript", response_model=TranscriptEvaluationResponse)
async def evaluate_transcript(request: TranscriptEvaluationRequest):
    try:
        prompt = create_prompt(request.transcript, request.ground_truth)

        response = openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": "You are an expert speech evaluator."},
                {"role": "user", "content": prompt},
            ],
        )

        feedback = response["choices"][0]["message"]["content"]

        return TranscriptEvaluationResponse(feedback=feedback)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
