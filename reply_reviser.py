import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Gemini Pro model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def revise_reply(draft, critique):
    prompt = f"""Here's an email reply draft:

{draft}

And here's some critique on it:

{critique}

Revise the reply to incorporate the feedback.
Just provide the revised reply email body without any additional text.
Dont add unkown names just use my name Shiva guptha in the Best regards section. 
And Also dont give multiple options, just give one final reply because I am using this in a web app and I need to show only one final reply to the user.
And also dont give any subject line, just give the body of the email.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
