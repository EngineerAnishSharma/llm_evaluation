# ===========================
# main.py
# ===========================
from dotenv import load_dotenv
load_dotenv()

import argparse
from loaders.chat_loader import load_chat_json, extract_last_user_message
from loaders.context_loader import load_context_json, get_top_k_contexts
from generation.build_prompt import build_prompt
from generation.generate_answer import generate_answer
from evaluation.relevance import compute_relevance
from evaluation.completeness_factuality import evaluate_completeness_and_factuality
from evaluation.latency_cost import get_tokens


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--top_k", type=int, default=5)

    args = parser.parse_args()

    chat_json = load_chat_json(args.chat)
    context_json = load_context_json(args.context)

    user_msg, _ = extract_last_user_message(chat_json)
    top_ctx = get_top_k_contexts(context_json, args.top_k)

    prompt = build_prompt(chat_json, top_ctx)

    print("Generating answer...")
    answer, latency, resp = generate_answer(prompt, args.model)

    print("Evaluating relevance...")
    rel = compute_relevance(answer, top_ctx)

    print("Evaluating completeness + factuality...")
    comp, fact, eval_resp = evaluate_completeness_and_factuality(
        answer, user_msg, top_ctx, args.model
    )

    print("\n==== RESULTS ====")
    print("User Message:", user_msg)
    print("Model Answer:", answer)
    print("Latency:", latency)
    print("Relevance:", rel)
    print("Completeness:", comp)
    print("Factuality:", fact)
    print("Gen Tokens:", get_tokens(resp))
    print("Eval Tokens:", get_tokens(eval_resp))
    print("=================")


if __name__ == "__main__":
    main()
