from services.llm_service import call_llm
from services.ner_service import extract_entities

def triage_message(message):
    
    classification_prompt = f"""
Classify this agriculture-related message:

Message: {message}

Return JSON:
{{
 "intent": "",
 "urgency": "low/medium/high"
}}
"""
    
    classification = call_llm(classification_prompt)

    entities = extract_entities(message)

    draft_prompt = f"""
Generate a professional agriculture support response.

Message: {message}
Intent + Urgency: {classification}

Response:
"""
    
    draft = call_llm(draft_prompt)

    return {
        "classification": classification,
        "entities": entities,
        "draft_response": draft
    }