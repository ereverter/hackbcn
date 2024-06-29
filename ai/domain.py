from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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


# hume


class HumeEmotion(BaseModel):
    name: str
    score: float


class HumeTime(BaseModel):
    begin: float
    end: float


class HumePrediction(BaseModel):
    text: str
    time: HumeTime
    confidence: Optional[float]
    emotions: List[HumeEmotion]
    speaker_confidence: Optional[float]


class HumeGroupedPrediction(BaseModel):
    id: str
    predictions: List[HumePrediction]


class HumeProsodyModel(BaseModel):
    metadata: Dict[str, Any]
    grouped_predictions: List[HumeGroupedPrediction]


class HumeModels(BaseModel):
    prosody: HumeProsodyModel


class HumeFilePrediction(BaseModel):
    file: str
    models: HumeModels


class HumeResult(BaseModel):
    predictions: List[HumeFilePrediction]


class HumeSource(BaseModel):
    type: str
    filename: str
    content_type: Optional[str]
    md5sum: str


class HumePredictionResponse(BaseModel):
    source: HumeSource
    results: HumeResult


class HumeResponse(BaseModel):
    predictions: List[HumePredictionResponse]
    errors: List[Any]
