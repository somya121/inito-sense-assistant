import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load Gemini Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Knowledge Base
with open("knowledge_base.json") as f:
    KB = json.load(f)

# Use SAFE model name
model = genai.GenerativeModel("gemini-2.5-flash")


SYSTEM_CONTEXT = """
You are Inito Sense, an expert in:
- Inito fertility monitor usage
- Hormone tracking (LH, E3G, PdG)
- Fertility education
- App troubleshooting

Always answer in context of Inito product.
"""

def build_context():
    text = ""
    for section in KB.values():
        text += "\n".join(section) + "\n"
    return text

def get_ai_response(user_message):
    
    full_prompt = SYSTEM_CONTEXT + build_context() + "\nUser: " + user_message

    response = model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.4
        )
    )

    return response.text
