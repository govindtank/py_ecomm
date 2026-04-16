import re
from typing import Any, Dict


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case string to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str: str) -> str:
    """Convert camelCase string to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_dict_keys_to_camel(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert all dictionary keys from snake_case to camelCase recursively."""
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        camel_key = to_camel_case(key)
        if isinstance(value, dict):
            result[camel_key] = convert_dict_keys_to_camel(value)
        elif isinstance(value, list):
            result[camel_key] = [
                convert_dict_keys_to_camel(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[camel_key] = value
    return result


def convert_dict_keys_to_snake(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert all dictionary keys from camelCase to snake_case recursively."""
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        snake_key = to_snake_case(key)
        if isinstance(value, dict):
            result[snake_key] = convert_dict_keys_to_snake(value)
        elif isinstance(value, list):
            result[snake_key] = [
                convert_dict_keys_to_snake(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[snake_key] = value
    return result
