# ===========================
# evaluation/relevance.py
# ===========================

from sentence_transformers import SentenceTransformer, util
import numpy as np

embed = SentenceTransformer('all-MiniLM-L6-v2')

def compute_relevance(answer, contexts):
    if not answer.strip():
        return {"max": 0.0, "avg": 0.0}

    ans_emb = embed.encode(answer, convert_to_tensor=True)

    scores = []
    for c in contexts:
        txt = c.get('text', '')
        if not txt:
            scores.append(0.0)
            continue
        ctx_emb = embed.encode(txt, convert_to_tensor=True)
        score = float(util.cos_sim(ans_emb, ctx_emb).item())
        scores.append(score)

    arr = np.array(scores)
    return {"max": float(arr.max()), "avg": float(arr.mean()), "list": scores}
