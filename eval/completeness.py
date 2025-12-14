from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def completeness_score(question, answer, model="gpt-4o-mini"):
    prompt = f"""
    Evaluate how completely the answer addresses the question.

    Question: {question}
    Model Answer: {answer}

    Return a score between 0 and 1:
    - 1 = fully complete answer
    - 0 = very incomplete or missing details

    Only return the numeric score.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content
    if content is None:
        return 0.0

    try:
        return float(content.strip())
    except:
        return 0.0
