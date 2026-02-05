def normalize_token(token: str) -> str:
    """
    Safe normalization:
    - strip whitespace
    - remove leading/trailing punctuation
    - lowercase ONLY for latin characters
    """
    token = token.strip()

    # remove common punctuation at edges
    token = token.strip(".,;:!?()[]{}\"'")

    # lowercase only if ASCII (safe for English)
    if token.isascii():
        token = token.lower()

    return token
