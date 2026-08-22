import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def answer_query(query: str, analysis: dict) -> str:

    system_prompt = """
You are a Senior Business Analyst.

Answer the user's question using ONLY the provided dataset analysis.

Be precise.
Use the model results, metrics, feature importance,
predictions, dataset statistics and business summary when relevant.

Do not invent numbers.
If the provided analysis does not contain enough information,
say so clearly.

Keep the answer concise and business-focused.
"""

    user_prompt = f"""
DATASET ANALYSIS:

{json.dumps(analysis, indent=2)}

USER QUESTION:

{query}

Answer the user's question.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content