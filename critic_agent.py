import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Gemini Pro model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def critique_reply(email_body, draft):
    prompt = f"""You are an expert email writer. Here's the original email:

{email_body}

And here's the draft reply:

{draft}

Critique the draft and suggest improvements."""
    response = model.generate_content(prompt)
    return response.text.strip()
