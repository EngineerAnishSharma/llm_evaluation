import time
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load API key before creating client
    
client = OpenAI()

def measure_latency(prompt, model="gpt-4o-mini"):
    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    end = time.time()
    latency = end - start

    answer = response.choices[0].message.content

    return answer, latency, response
