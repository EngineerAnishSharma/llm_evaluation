def calculate_cost(response):
    usage = response.usage
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    total_tokens = input_tokens + output_tokens

    # NOTE:
    # Add real pricing here later

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }
