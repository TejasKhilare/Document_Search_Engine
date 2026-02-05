def highlight_text(text, query_tokens):
    for token in query_tokens:
        text = text.replace(
            token,
            f"<<{token}>>"
        )
    return text
