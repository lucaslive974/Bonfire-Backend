def normalize_auto_infraction_id(ai: str) -> str:
    if not ai:
        return ai

    if "-" in ai:
        return ai

    if ai[len(ai) - 1] == "-":
        return ai

    return f"{ai[:-1]}-{ai[-1]}"
