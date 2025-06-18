import os
from nlp import analyze_email_context
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel(model_name="gemini-2.0-flash")


def draft_reply(email_body):

    context=analyze_email_context(email_body)

    if context["email_type"]=="reply" or context["email_type"]=="escalate":
        polite_adjective = context["email_type"]
    else:
        polite_adjective = ""    

    prompt = f"""Write a polite and {polite_adjective} email reply to the email below and My name is Shiva guptha add it Best regards section:\n\n Email:\n{email_body}"""
    response = model.generate_content(prompt)
    return response.text
