import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Intent classifier using zero-shot learning
intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Email type classifier via rule-based keywords (simple approach)
EMAIL_TYPES = {
    "personal": ["friend", "how are you", "long time", "family", "catch up"],
    "professional": ["interview", "project", "feedback", "meeting", "resume"],
    "marketing": ["sale", "offer", "discount", "unsubscribe", "buy now", "limited time"],
    "spam": ["prize", "lottery", "winner", "claim now", "urgent response"]
}


def extract_entities(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "DATE": [],
        "TIME": [],
        "TASKS": []
    }

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    # Heuristic task extraction: look for "to-do" patterns
    tasks = re.findall(r'\b(?:please|kindly|make sure to|you need to|todo) (.+?)(?:\.|\n|$)', text, flags=re.IGNORECASE)
    if tasks:
        entities["TASKS"].extend(tasks)

    return entities


def classify_intent(text):
    labels = ["reply", "ignore", "escalate"]
    result = intent_classifier(text, candidate_labels=labels)
    return result["labels"][0], result["scores"][0]


def classify_email_type(text):
    text_lower = text.lower()
    scores = {k: sum(word in text_lower for word in v) for k, v in EMAIL_TYPES.items()}
    best_type = max(scores, key=scores.get)
    return best_type


def analyze_email_context(email_body):
    print("\n📨 ANALYZING EMAIL CONTEXT...\n")

    entities = extract_entities(email_body)
    intent, confidence = classify_intent(email_body)
    email_type = classify_email_type(email_body)

    context = {
        "intent": intent,
        "intent_confidence": round(confidence, 2),
        "entities": entities,
        "email_type": email_type,
    }

    return context


# === Sample Usage ===

if __name__ == "__main__":
    sample_email = """
    Hi Shiva,

    Thanks for sending the report on the RISC-V processor. Please ensure you add the performance comparison chart before Friday.

    Let’s also schedule a review meeting next Tuesday at 2 PM with the ECE project group.

    Regards,
    Dr. Mehta
    """

    context = analyze_email_context(sample_email)
    print("\n📊 Email Context Result:")
    # print(context["intent"])
    for k, v in context.items():
        print(f"{k}: {v}")
