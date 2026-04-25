import re

def extract_entities(text):
    ids = re.findall(r'\b[A-Z0-9]{5,}\b', text)
    dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)

    return {
        "ids": ids,
        "dates": dates
    }