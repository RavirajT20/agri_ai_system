from services.llm_service import call_llm
import json
import re
import random

# 🔹 Utility: Clean & Parse JSON safely
def extract_json(response):
    try:
        cleaned = re.search(r'\{.*\}', response, re.DOTALL).group()
        return json.loads(cleaned)
    except:
        return None


# 🔹 Step 1: Generate Dynamic Question (Unique + Random)
def generate_question(previous_questions=None):

    if previous_questions is None:
        previous_questions = []

    random_seed = random.randint(1, 100000)

    prompt = f"""
You are an Agriculture Tutor AI.

Generate ONE completely NEW and UNIQUE agriculture question.

STRICT RULES:
- Do NOT repeat previous questions
- Use different topics every time (soil, irrigation, pests, fertilizers, climate, crops, etc.)
- Topic must be short (1-3 words)
- Fact must be scientifically correct
- Question must test understanding (not definition only)

Previous Questions:
{previous_questions}

Random Seed: {random_seed}

Return ONLY valid JSON:
{{
 "topic": "short topic name",
 "fact": "a correct agriculture fact",
 "question": "ask user a question based on fact"
}}
"""

    for _ in range(3):  # 🔁 Retry logic
        response = call_llm(prompt)
        parsed = extract_json(response)

        if parsed and all(k in parsed for k in ["topic", "fact", "question"]):

            # 🚫 Avoid duplicates
            if parsed["question"] not in previous_questions:
                return parsed

    return {
        "error": "Failed to generate a unique question. Please try again."
    }


# 🔹 Step 2: Evaluate Answer
def evaluate_answer(topic, fact, user_answer):

    prompt = f"""
You are an Agriculture Tutor AI.

Topic: {topic}
Correct Fact: {fact}
User Answer: {user_answer}

Evaluate strictly based on the fact.

RULES:
- Score must be between 0 to 10
- Be strict but fair
- Give clear reasoning

Return ONLY valid JSON:
{{
 "score": 0-10,
 "is_correct": true/false,
 "correct_answer": "clear correct explanation",
 "explanation": "why user is right or wrong",
 "improvement": "how to improve the answer"
}}
"""

    for _ in range(3):  # 🔁 Retry logic
        response = call_llm(prompt)
        parsed = extract_json(response)

        if parsed and "score" in parsed:
            return parsed

    return {
        "score": 0,
        "is_correct": False,
        "correct_answer": "Could not evaluate",
        "explanation": "LLM response parsing failed",
        "improvement": "Try again"
    }