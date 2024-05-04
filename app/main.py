from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

app = FastAPI()


# Define the request model for the endpoint
class EvaluateRequest(BaseModel):
    model: str = Field(
        ...,
        example="whisper-small",
        description="The model to evaluate, either 'whisper-small' or 'whisper-tiny'.",
    )
    created_from_date: date = Field(
        ...,
        example="2023-01-01",
        description="The minimum date of the recordings to evaluate.",
    )
    created_to_date: date = Field(
        ...,
        example="2023-01-10",
        description="The maximum date of the recordings to evaluate.",
    )
    user_id: int = Field(
        None, example=123, description="Filter recordings to evaluate by user id."
    )
    unit_id: int = Field(
        None, example=456, description="Filter recordings to evaluate by unit id."
    )


# Define the response model for the endpoint
class EvaluationResponse(BaseModel):
    wer: float = Field(
        ..., example=0.05, description="Word Error Rate of the model on the dataset."
    )


def load_model(model_name: str):
    if model_name not in ["whisper-small", "whisper-tiny"]:
        raise ValueError("Model not supported")
    return pipeline("automatic-speech-recognition", model=model_name)


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: EvaluateRequest):
    try:
        # Load the specified model
        asr_model = load_model(request.model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Here we would fetch and filter the dataset based on `created_from_date`, `created_to_date`, `user_id`, `unit_id`.
    # For now, we're just simulating an evaluation.

    # Simulate fetching data and performing the evaluation
    # This part should interact with actual data and compute WER
    simulated_wer = 0.05  # Example WER, this should be computed based on actual data

    return EvaluationResponse(wer=simulated_wer)
