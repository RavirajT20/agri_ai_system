from fastapi import APIRouter
from agents.education_agent import generate_question, evaluate_answer

router = APIRouter()

# 🔹 Get Question

# 🔹 Evaluate Answer
@router.post("/evaluate")
def evaluate(data: dict):
    result = evaluate_answer(
        data["topic"],
        data["fact"],
        data["user_answer"]
    )
    return result   # ✅ directly return JSON (NOT string)

question_history = []

@router.get("/question")
def get_question():
    q = generate_question(question_history)

    if "question" in q:
        question_history.append(q["question"])

    return q