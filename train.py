import os
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ml.features import extract_features
from ml.model import CLASSES, TremorFeatureNet
from ml.signal import resample_signal

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = Path(os.environ.get("MODEL_PATH", ROOT / "artifacts" / "signals.pt"))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = None
model_version = None
feature_mean = None
feature_scale = None

app = FastAPI(title="TremorScan research inference", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Sample(BaseModel):
    t: float
    x: float
    y: float
    z: float


class InferenceRequest(BaseModel):
    task: str = Field(pattern="^(rest|postural|kinetic)$")
    sample_rate_hz: float = Field(gt=0, le=250)
    samples: list[Sample] = Field(min_length=100, max_length=5000)


@app.on_event("startup")
def load_model():
    global model, model_version, feature_mean, feature_scale

    if not MODEL_PATH.is_file():
        return

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True,
    )
    network = TremorFeatureNet()
    network.load_state_dict(checkpoint["state_dict"])
    network.eval().to(DEVICE)

    model = network
    model_version = checkpoint.get("version", "unversioned")
    feature_mean = np.asarray(checkpoint["feature_mean"], dtype=np.float32)
    feature_scale = np.asarray(checkpoint["feature_scale"], dtype=np.float32)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/model")
def model_status():
    return {
        "ready": model is not None,
        "name": (
            "Two-feature neural network"
            if model is not None
            else "No trained checkpoint installed"
        ),
        "version": model_version,
        "classes": CLASSES,
    }


@app.post("/api/inference")
def inference(payload: InferenceRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="No trained model checkpoint is installed.",
        )

    samples = sorted(payload.samples, key=lambda item: item.t)
    times = np.asarray([sample.t for sample in samples], dtype=np.float64)
    axes = np.asarray(
        [[sample.x, sample.y, sample.z] for sample in samples],
        dtype=np.float32,
    )

    if not np.isfinite(axes).all() or not np.isfinite(times).all():
        raise HTTPException(
            status_code=422,
            detail="Signal values must be finite.",
        )
    if np.any(np.diff(times) <= 0):
        raise HTTPException(
            status_code=422,
            detail="Sample timestamps must be unique and increasing.",
        )

    duration = (times[-1] - times[0]) / 1000.0
    if duration < 9.0:
        raise HTTPException(
            status_code=422,
            detail="At least nine seconds of motion data are required.",
        )

    signal = resample_signal(times, axes, sample_rate=50.0, length=475)
    features = extract_features(signal, sample_rate_hz=50.0)
    features = (features - feature_mean) / feature_scale

    with torch.inference_mode():
        logits = model(torch.from_numpy(features).unsqueeze(0).to(DEVICE))
        probabilities = torch.softmax(logits, dim=1)[0].cpu().numpy()

    index = int(np.argmax(probabilities))
    return {
        "label": CLASSES[index],
        "score": float(probabilities[index]),
        "probabilities": {
            name: float(value)
            for name, value in zip(CLASSES, probabilities)
        },
        "interpretation": (
            "Research model output only. This result is not a diagnosis or "
            "a clinical risk estimate."
        ),
        "model_version": model_version,
        "task": payload.task,
    }
