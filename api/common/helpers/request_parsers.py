import types

from fastapi.exceptions import HTTPException
from fastapi import status as status_codes


def get_json_key_or_raise_400(
        json_payload: dict,
        required: list,
        optional: list = None,
        validators: dict[str, (..., bool)] = None
):
    """
    Extracts keys from a JSON payload and performs validation.

    This function takes a JSON payload and extracts the keys specified in the 'required' list.
    It also performs optional validation using validators provided in the 'validators' dictionary.

    Parameters:
    - json_payload (dict): The JSON payload to extract keys from.
    - required (list): A list of required keys.
    - optional (list, optional): A list of optional keys. Defaults to None.
    - validators (dict[str, (...,bool)], optional): A dictionary of validators for each key.
      The validators should return a tuple with a boolean indicating validation status and an optional error message.
      Defaults to None.

    Returns:
    - list: A list containing the extracted values corresponding to the required keys.

    Raises:
    - TypeError: If 'json_payload' is not a dictionary.

    Examples:
    ```
    json_payload = {'key1': 'value1', 'key2': 'value2'}
    required = ['key1']
    optional = ['key2']
    validators = {'key1': lambda x: (True, None)}
    result = get_json_key_or_raise_400(json_payload, required, optional, validators)
    ```
    """

    # Initialize validators if None
    if validators is None:
        validators = {}

    # Check if json_payload is a dictionary
    if not isinstance(json_payload, dict):
        raise TypeError(f"json_payload must be dict not {type(json_payload)}")

    # Initialize optional list if None
    if optional is None:
        optional = []

    results = []
    keys_not_found = []
    keys_invalid = []

    # Iterate through required keys
    for key in required:
        results.append(json_payload.get(key))
        # Check if required key is missing and not in optional list
        if key not in json_payload.keys() and key not in optional:
            keys_not_found.append(key)
            continue
        # Check if validator exists for the key and perform validation
        if key in validators.keys() and key not in keys_not_found:
            try:
                validator = validators.get(key)
                status, _err = validator(json_payload.get(key))
                if not status:
                    keys_invalid.append(f"<{key}> err: {_err}")
            except Exception as e:
                keys_invalid.append(f"<{key}> err: {str(e)}")

    # Raise 400 error if required keys are missing
    if keys_not_found:
        raise HTTPException(status_codes.HTTP_400_BAD_REQUEST, f"the following required perimeter is missing:\n {str(keys_not_found)}")

    # Raise 400 error if any key is invalid
    if keys_invalid:
        raise HTTPException(status_codes.HTTP_400_BAD_REQUEST, f"bad peremiter: \n {str(keys_invalid)}")

    return results
