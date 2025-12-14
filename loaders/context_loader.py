# ===========================
# loaders/context_loader.py
# ===========================

def load_context_json(path):
    import json
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_top_k_contexts(context_json, top_k):
    vector_data = context_json.get('data', {}).get('vector_data', [])
    return vector_data[:top_k]


