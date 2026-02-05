from typing import List, Tuple

def tokenize(text: str) -> List[Tuple[str, int]]:
    tokens = text.split()
    return [(token, idx) for idx, token in enumerate(tokens)]
