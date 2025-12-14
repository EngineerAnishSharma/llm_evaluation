# LLM Evaluation Toolkit

End to end script to generate an LLM answer from chat history plus retrieved context, then score it for relevance, completeness, factuality, latency, and token cost. Works with OpenAI chat completions and SentenceTransformer embeddings.

## What it does
- Loads a chat transcript and context vectors from JSON files.
- Builds a retrieval augmented prompt from recent turns and top K contexts.
- Calls an OpenAI chat model to generate an answer and measures latency + tokens.
- Scores the answer for semantic relevance against each context snippet.
- Asks the LLM to judge completeness and factuality with respect to the provided context only.
- Prints a compact report with all metrics.

## Repository map
- [main.py](main.py): CLI orchestrator; ties loaders, generation, and evaluation together.
- [generation/build_prompt.py](generation/build_prompt.py): Constructs the final prompt from chat history and context snippets.
- [generation/generate_answer.py](generation/generate_answer.py): Calls OpenAI chat completions and returns answer + latency + raw response.
- [loaders/chat_loader.py](loaders/chat_loader.py): Reads chat JSON and extracts the latest user message.
- [loaders/context_loader.py](loaders/context_loader.py): Reads context JSON and returns top K vector entries.
- [evaluation/relevance.py](evaluation/relevance.py): Computes cosine similarity between the answer and each context snippet via all-MiniLM-L6-v2.
- [evaluation/completeness_factuality.py](evaluation/completeness_factuality.py): Prompts the LLM to return JSON scores for completeness and factuality.
- [evaluation/latency_cost.py](evaluation/latency_cost.py): Helper to extract token counts from OpenAI responses.
- [eval/*](eval): Earlier standalone metrics (completeness, hallucination, relevance, latency, cost) kept for reference.
- Sample data: [sample-chat-conversation-01.json](sample-chat-conversation-01.json), [sample-chat-conversation-02.json](sample-chat-conversation-02.json), [sample_context_vectors-01.json](sample_context_vectors-01.json), [sample_context_vectors-02.json](sample_context_vectors-02.json).

## Data formats
Chat JSON (truncated example):
```json
{
	"conversation_turns": [
		{"role": "user", "message": "Hi"},
		{"role": "assistant", "message": "Hello"},
		{"role": "user", "message": "What is retrieval augmented generation?"}
	]
}
```

Context JSON (truncated example):
```json
{
	"data": {
		"vector_data": [
			{"id": "ctx1", "text": "RAG uses external documents to ground LLM responses."},
			{"id": "ctx2", "text": "It retrieves top-k passages before generation."}
		]
	}
}
```

## Prerequisites
- Python 3.9+
- OpenAI API key in environment variable `OPENAI_API_KEY` (loaded via python-dotenv if present in a `.env` file).
- `pip install -r requirements.txt` (or install equivalents):
	- openai
	- python-dotenv
	- sentence-transformers
	- numpy

## Running the pipeline
Basic invocation:
```bash
python main.py --chat sample-chat-conversation-01.json --context sample_context_vectors-01.json --model gpt-4o-mini --top_k 5
```

Output fields:
- User Message: last user turn extracted from the chat file.
- Model Answer: generated reply grounded on provided context.
- Latency: end to end OpenAI call duration in seconds.
- Relevance: max/avg cosine similarity of answer vs contexts.
- Completeness: LLM-judged coverage of the question (0-1).
- Factuality: LLM-judged grounding against context only (0-1).
- Gen Tokens / Eval Tokens: prompt + completion token counts for generation and evaluation calls.

## How it works (flow)
1) Load chat + context JSON.
2) Extract the last user question and top K context snippets.
3) Build a retrieval augmented prompt (history + labeled context blocks + safety instruction).
4) Generate an answer via OpenAI and time the call.
5) Score semantic relevance with SentenceTransformer cosine similarity.
6) Ask the LLM to return JSON `{ "completeness": x, "factuality": y }` for the answer conditioned on the same contexts.
7) Report metrics and token usage.

## Notes and limits
- Context text is truncated to ~500 characters per snippet before evaluation to keep prompts small.
- Relevance embeddings run locally; completeness/factuality rely on the model specified by `--model`.
- Replace pricing logic in [eval/cost.py](eval/cost.py) with your own rates if you use the legacy helpers.

## Extending
- Swap `--model` to target a different OpenAI model; ensure it supports chat completions.
- Adjust prompt construction in [generation/build_prompt.py](generation/build_prompt.py) to add system rules or citations.
- Add new metrics by extending the `evaluation` module and wiring into [main.py](main.py).
