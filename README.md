# FebrabanCode Class

The `FebrabanCode` class is designed to parse and validate Febraban codes commonly used in Brazil, such as bar codes and lines. This class provides methods to extract information from Febraban codes, validate their integrity, and retrieve specific details.

## Usage

To use this class, follow these steps:

1. **Instantiate the Class**: Create an instance of the `FebrabanCode` class by passing the Febraban code (either bar or line) as a string parameter.

2. **Retrieve Information**: Utilize the provided methods to retrieve information from the Febraban code, such as bank details, currency, value, and expiration date.

3. **Validation**: Use the `validate()` method to check the integrity of the provided Febraban code. This method validates the control digits and ensures the code's correctness.

## Class Methods

### `__init__(bar_code: str)`

Constructor method to initialize the `FebrabanCode` object. It takes a Febraban code (either bar or line) as input.

### `get_code_info() -> Dict[str, Union[str, date, float]]`

Returns a dictionary containing information extracted from the Febraban code, including bank details, currency, expiration date, and value.

### `get_bar() -> str`

Returns the Febraban bar code as a string.

### `get_line(formatted: bool = False) -> str`

Returns the Febraban line code as a string. If `formatted` is set to `True`, the line code is returned with formatting for readability.

### `validate() -> bool`

Validates the integrity of the Febraban code. Returns `True` if the code is valid, otherwise `False`.

## Internal Methods

### `__code_match(code: str) -> str`

Internal method to match and sanitize the input Febraban code.

### `__get_dv_module_10(number: str) -> int`

Calculates the verification digit using the module 10 algorithm.

### `__get_dv_module_11(number: str) -> int`

Calculates the verification digit using the module 11 algorithm.

### `__get_expiry(expiry_factor: str) -> date`

Calculates the expiration date based on the provided expiration factor.

### `__convert_value_factor(value: str) -> float`

Converts the value factor from the Febraban code to a float value.

### `__get_info_from_line(line: str) -> Dict[str, Union[str, date, float]]`

Extracts information from the line code of the Febraban code.

### `__get_info_from_bar(bar: str) -> Dict[str, Union[str, date, float]]`

Extracts information from the bar code of the Febraban code.

### `__get_info_from_code(code: str) -> Dict[str, Union[str, date, float]]`

Determines the type of Febraban code (bar or line) and extracts information accordingly.

## Error Handling

- Raises `AttributeError` if the provided input is not a string.
- Raises `ValueError` if the length of the code is not valid (either 47 digits for the line or 44 digits for the bar).

## Dependencies

- `datetime`: Standard Python library for date and time operations.
- `timedelta`: Standard Python library for representing differences between dates or times.
- `re`: Standard Python library for regular expressions.
- `typing`: Standard Python library for type hints.

## Example

```python
from febraban_code import FebrabanCode

# Instantiate with a Febraban code
febraban_code = FebrabanCode("34191091001219011004141140141141000000120100")

# Retrieve information
info = febraban_code.get_code_info()
print(info)

# Validate the code
is_valid = febraban_code.validate()
print(is_valid)
