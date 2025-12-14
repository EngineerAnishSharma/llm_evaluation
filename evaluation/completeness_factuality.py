# ===============================================
# evaluation/completeness_factuality.py
# ===============================================

import json
from openai import OpenAI

client = OpenAI()

def evaluate_completeness_and_factuality(answer, question, contexts, model="gpt-4o-mini"):
    ctx_text = "\n".join([c.get('text', '')[:500] for c in contexts])

    eval_prompt = f"""
Return a JSON only:
{{"completeness":0-1, "factuality":0-1}}

Definitions:
- completeness: how fully the answer solves the user's question.
- factuality: supported by these context snippets only.

Question: {question}
Answer: {answer}
Context:
{ctx_text}
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0
    )

    raw = resp.choices[0].message.content or ""
    try:
        data = json.loads(raw)
        return data.get("completeness", 0.0), data.get("factuality", 0.0), resp
    except:
        return 0.0, 0.0, resp