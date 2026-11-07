import math
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Calculator")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class Calculation(BaseModel):
    left: float = Field(allow_inf_nan=False)
    right: float = Field(allow_inf_nan=False)
    operator: Literal["+", "-", "*", "/"]


class CalculationResult(BaseModel):
    result: float


@app.get("/", include_in_schema=False)
def calculator_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/calc", response_model=CalculationResult)
def calculate(calculation: Calculation) -> CalculationResult:
    left = calculation.left
    right = calculation.right

    if calculation.operator == "+":
        result = left + right
    elif calculation.operator == "-":
        result = left - right
    elif calculation.operator == "*":
        result = left * right
    else:
        if right == 0:
            raise HTTPException(status_code=422, detail="Cannot divide by zero")
        result = left / right

    if not math.isfinite(result):
        raise HTTPException(status_code=422, detail="Result is outside the supported numeric range")

    return CalculationResult(result=result)
