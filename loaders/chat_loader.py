# =========================
# loaders/chat_loader.py
# =========================

def load_chat_json(path):
    import json
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_last_user_message(chat_json):
    turns = chat_json.get('conversation_turns', [])
    for t in reversed(turns):
        role = t.get('role', '').lower()
        if role == 'user':
            return t.get('message', ''), t
    if turns:
        return turns[-1].get('message', ''), turns[-1]
    return '', {}


