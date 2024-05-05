from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uniplot import histogram

from backend.pipeline import main

app = FastAPI()


class EvaluateRequest(BaseModel):
    model: str = Field(
        ...,
        example="whisper-small",
        description="The model to evaluate, either 'whisper-small' or 'whisper-tiny'.",
    )
    created_from_date: str = Field(
        None,
        example="2023-01-01",
        description="The minimum date of the recordings to evaluate.",
    )
    created_to_date: str = Field(
        None,
        example="2023-01-10",
        description="The maximum date of the recordings to evaluate.",
    )
    user_id: int = Field(
        None, example=2, description="Filter recordings to evaluate by user id."
    )
    unit_id: int = Field(
        None, example=3, description="Filter recordings to evaluate by unit id."
    )


# Define the response model for the endpoint
class EvaluationResponse(BaseModel):
    wer: float = Field(
        ..., example=0.05, description="Word Error Rate of the model on the dataset."
    )


@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    try:
        result = main(
            model_id=request.model,
            created_from_date=request.created_from_date,
            created_to_date=request.created_to_date,
            user_id=request.user_id,
            unit_id=request.unit_id,
        )

        return result
    except Exception as e:
        return {"error": str(e)}
