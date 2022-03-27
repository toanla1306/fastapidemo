from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    task_id: str
    status: str

class Prediction(BaseModel):
    task_id: str
    status: str

class ParamsPredict(BaseModel):
    project_name: str
    param_predict_1: Optional[str] = None
    param_predict_2: str
    param_predict_3: str
