# ===========================
# generation/build_prompt.py
# ===========================

def build_prompt(chat_json, contexts):
    turns = chat_json.get('conversation_turns', [])
    history = []

    for t in turns[-10:]:
        history.append(f"{t.get('role', 'User')}: {t.get('message', '')}")

    ctx_block = []
    for i, c in enumerate(contexts, 1):
        ctx_block.append(f"Context {i}:\n{c.get('text', '')}\n")

    prompt = (
        "You are an AI assistant. Use context + history. Avoid hallucination.\n\n"
        f"Conversation History:\n{'\n'.join(history)}\n\n"
        f"Context Snippets:\n{'\n---\n'.join(ctx_block)}\n"
        "Answer strictly based on context or say 'Not enough information'."
    )

    return prompt
