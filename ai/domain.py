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


# hume
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class HEmotion(BaseModel):
    name: str
    score: float

class HTime(BaseModel):
    begin: float
    end: float

class HPrediction(BaseModel):
    text: str
    time: HTime
    confidence: Optional[float]
    emotions: List[HEmotion]
    speaker_confidence: Optional[float]

class HGroupedPrediction(BaseModel):
    id: str
    predictions: List[HPrediction]

class HProsodyModel(BaseModel):
    metadata: Dict[str, Any]
    grouped_predictions: List[HGroupedPrediction]

class HModels(BaseModel):
    prosody: HProsodyModel

class HFilePrediction(BaseModel):
    file: str
    models: HModels

class HResult(BaseModel):
    predictions: List[HFilePrediction]

class HSource(BaseModel):
    type: str
    filename: str
    content_type: Optional[str]
    md5sum: str

class HPredictionResponse(BaseModel):
    source: HSource
    results: HResult

class HumeResponse(BaseModel):
    predictions: List[HPredictionResponse]
    errors: List[Any]
