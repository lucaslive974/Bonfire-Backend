from typing import Any, List

from exceptions.CustomExceptions import ErrIncompleteData, ErrInvalidJson


def checkKeysInJson(
    jsonObject: List[Any], keys_to_check: List[str], expectedObject: str
) -> None:
    """Verifica se os dados necessários estão no JSON."""
    if not jsonObject:
        raise ErrInvalidJson(expectedObject, "Envie um JSON válido", 400)

    missing_keys = []
    for item in jsonObject:
        if isinstance(item, dict):
            missing_keys_item = [key for key in keys_to_check if key not in item]
            if missing_keys_item:
                missing_keys.extend(missing_keys_item)

    if missing_keys:
        raise ErrIncompleteData(f"Certifique-se de incluir {missing_keys}", 401)
