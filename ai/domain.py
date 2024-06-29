from pydantic import BaseModel
from typing import List

class VideoInput(BaseModel):
    video: str

class AudioInput(BaseModel):
    audio: str

class AudioTranscript(BaseModel):
    transcript: List[str]
    timestamps: List[str]
    emotions: List[str]

class VideoFrames(BaseModel):
    frames: List[str]

class FramesBodyLangyage(BaseModel):
    frames: List[str]
    body_language: List[str]

class GroundTranscript(BaseModel):
    transcript: str

class PresentationEvaluation(BaseModel):
    evaluation: str
    