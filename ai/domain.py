from typing import Any, Dict, List, Optional

from pydantic import BaseModel

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
    speaker_confidence: Optional[float]
    emotions: List[HumeEmotion]


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
    file_type: Optional[str]
    models: HumeModels


class HumeResult(BaseModel):
    predictions: List[HumeFilePrediction]


class HumeSource(BaseModel):
    type: str
    filename: Optional[str]
    content_type: Optional[str]
    md5sum: Optional[str]


class HumePredictionResponse(BaseModel):
    source: HumeSource
    results: HumeResult


class HumeResponse(BaseModel):
    predictions: List[HumePredictionResponse]
    errors: List[Any]


# openai


class TranscriptEvaluationRequest(BaseModel):
    transcript: List[Any]
    ground_truth: str


class TranscriptEvaluationResponse(BaseModel):
    feedback: str
