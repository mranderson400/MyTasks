from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
import spacy
from datetime import datetime, timedelta
import random
from bson import ObjectId
import dateparser

from models.task_model import Task

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

router = APIRouter()

# Extract due date using dateparser (handles natural phrases)
def extract_due_date(text: str):
    doc = nlp(text)
    text_lower = text.lower()

    # Dynamically decide whether to prefer past or future
    if any(word in text_lower for word in ["before", "ago", "last"]):
        preference = "past"
    elif any(word in text_lower for word in ["after", "in", "next", "upcoming"]):
        preference = "future"
    else:
        preference = "future"  # Default

    settings = {
        "RELATIVE_BASE": datetime.now(),
        "PREFER_DATES_FROM": preference
    }

    # Try parsing entities with spaCy first
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed = dateparser.parse(ent.text, settings=settings)
            if parsed:
                return parsed

    # Fallback to full sentence
    fallback = dateparser.parse(text, settings=settings)
    return fallback

# Extract status from the text using keyword match
def extract_status(text: str):
    status_keywords = {
        "Pending": ["not started", "yet to begin", "pending"],
        "In Progress": ["in progress", "ongoing", "work has started", "currently doing"],
        "Completed": ["done", "completed", "finished"]
    }
    lowered = text.lower()
    for status, keywords in status_keywords.items():
        if any(kw in lowered for kw in keywords):
            return status
    return random.choice(["Pending", "In Progress", "Completed"])

# Task creation endpoint
@router.post("/chatbot/create")
async def create_task(request: Request, description: str = Form(...)):
    user = request.session.get("user")

    doc = nlp(description)

    # Use first full sentence as title if available
    sentences = list(doc.sents)
    title = sentences[0].text.strip() if sentences else doc[:5].text

    # Parse due date from description
    due_date = extract_due_date(description)
    if not due_date:
        due_date = datetime.today() + timedelta(days=7)

    # Extract status
    status = extract_status(description)

    # Create task payload
    task_data = {
        "title": title,
        "description": description,
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": status,
        "user_id": ObjectId(user["_id"]),
    }

    Task.create_task(task_data)
    return RedirectResponse(url="/welcome", status_code=303)