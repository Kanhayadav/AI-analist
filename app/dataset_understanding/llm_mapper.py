import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a Senior Data Engineer. Your task is to classify business dataset columns.
Map EVERY single input column to EXACTLY ONE of these labels:
- Revenue
- Cost
- Profit
- Quantity
- Price
- Date
- CustomerID
- Unknown

Rules:
1. Never invent a new label. If a column doesn't fit, map it to 'Unknown'.
2. Return JSON exactly like this:

{
    "ColumnName": {
        "mapped_to": "Revenue",
        "confidence": 0.98,
        "reason": "Represents sales."
    }
}

Every input column must appear exactly once.
Return ONLY JSON.
3. Do not include markdown formatting or backticks. Return ONLY raw JSON.
"""

def llm_column_mapper(columns):
    # Constructing standard chat payload
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Columns to map:\n{columns}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",          # CHANGE 1: Switched to mini model (fraction of the cost)
            messages=messages,
            response_format={"type": "json_object"}, # CHANGE 2: Forces strict JSON mode to avoid useless word costs
            max_completion_tokens=500     # CHANGE 3: Limits response size so an error doesn't burn credits
        )
        
        # CHANGE 4: Fixed standard SDK extraction pathway
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:

        print(e)

        return {
            col: {
                "mapped_to":"Unknown",
                "confidence":0.0,
                "reason":"Failed to parse"
            }
            for col in columns
        }