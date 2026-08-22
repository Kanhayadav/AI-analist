import json
from openai import OpenAI
from app.config import OPENAI_API_KEY
from .prompt import SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_user_query(user_query, columns):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Dataset Columns:\n{columns}\n\nUser Query:\n{user_query}"}
    ]

    # 2. Use standard API call structure optimized for cost
    response = client.chat.completions.create(
        model="gpt-4o-mini",          
        messages=messages,
        response_format={"type": "json_object"}, # CHANGE 2: Forces strict JSON, saving tokens on conversational fluff
        max_completion_tokens=250     # CHANGE 3: Caps runaway responses to save money if something goes wrong
    )

    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, AttributeError, KeyError):
        return {
            "target": None,
            "task": None,
            "forecast_horizon": None,
            "filters": [],
            "confidence": 0.0
        }
