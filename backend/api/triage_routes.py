from fastapi import APIRouter
from models.schemas import TriageRequest
from agents.triage_agent import triage_message

router = APIRouter()

@router.post("/triage")
def triage(req: TriageRequest):
    result = triage_message(req.message)
    return result