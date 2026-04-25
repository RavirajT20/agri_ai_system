from pydantic import BaseModel

class EducationRequest(BaseModel):
    topic: str
    fact: str
    user_answer: str

class TriageRequest(BaseModel):
    message: str