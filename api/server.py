"""Server module to expose the Secret Santa module to the internet through an API."""

import os
import sys
from pathlib import Path

import pandas as pd
from fastapi import FastAPI

APP_PATH = Path(__file__).resolve().parents[1]
sys.path.append(os.path.join(APP_PATH, "secret_santa"))

import secret_santa


sample_participants = pd.read_csv(os.path.join(APP_PATH, "data", "example.csv"))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Ho ho ho! Merry XMas!"}


@app.get("/example/simple-shuffle")
async def run_example_simple_shuffle():
    pairs = secret_santa.shuffle(sample_participants)
    return {"pairs": [{"giver": pair.giver, "receiver": pair.receiver} for pair in pairs]}


@app.get("/example/complex-shuffle")
async def run_example_complex_shuffle():
    pairs = secret_santa.shuffle(sample_participants, simple_mode=False)
    return {"pairs": [{"giver": pair.giver, "receiver": pair.receiver} for pair in pairs]}
