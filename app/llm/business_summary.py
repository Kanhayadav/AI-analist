import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def explain_results(
    query_report: dict,
    training_report: dict,
    feature_selection_report: dict
) -> str:
    importance = feature_selection_report.get("feature_importance", {})
    training_summary = {
    "best_model": training_report["best_model_name"],
    "model_path": training_report["model_path"],
    "metrics": training_report["metrics"]
}
    system_prompt = (
        "You are a Senior Business Analyst. "
        "Explain machine learning results clearly and concisely to a business executive."
    )
    
    user_prompt = f"""
User Query / Task context:
{json.dumps(query_report, indent=2)}

Training Results:
{json.dumps(training_summary, indent=2)}

Important Features:
{json.dumps(importance, indent=2)}

Please write a business-ready summary covering:
1. Executive Summary
2. Model Performance
3. Most Important Business Drivers
4. Business Recommendation

Constraint: Maximum 250 words.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content