from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Load API key before creating client

client = OpenAI()

def hallucination_score(question, answer, model="gpt-4o-mini"):
    prompt = f"""
    Evaluate if the model's answer is factually correct.

    Question: {question}
    Model Answer: {answer}

    Give a score between 0 and 1:
    - 1 means fully correct
    - 0 means hallucinated or factually wrong

    Only return the number.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Safely extract content
    content = response.choices[0].message.content

    if content is None:
        return 0.0  # safest fallback

    content = content.strip()

    try:
        return float(content)
    except:
        return 0.0
