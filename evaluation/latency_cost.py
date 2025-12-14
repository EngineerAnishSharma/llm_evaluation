# ===========================
# evaluation/latency_cost.py
# ===========================

def get_tokens(resp):
    try:
        usage = resp.usage
        return {
            "input": usage.prompt_tokens,
            "output": usage.completion_tokens,
            "total": usage.prompt_tokens + usage.completion_tokens
        }
    except:
        return {"input": 0, "output": 0, "total": 0}
