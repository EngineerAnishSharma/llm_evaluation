# ================================
# generation/generate_answer.py
# ================================

from openai import OpenAI
import time
client = OpenAI()

def generate_answer(prompt, model="gpt-4o-mini"):
    start = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0
    )
    end = time.time()
    latency = end - start

    content = resp.choices[0].message.content or ""
    return content, latency, resp