from datetime import datetime, timedelta, date
from typing import Dict, Union
import re


class FebrabanCode:

    def __init__(self, bar_code: str) -> None:
        """
        - bar_code : str
            The barcode string to initialize the FebrabanCode object.
        """
        self.__code_info = self.__get_info_from_code(self.__code_match(bar_code))

    def __code_match(self, code: str) -> Dict[str, str]:
        """
        - code : str
            The barcode/line string to be matched.

        Returns the matched barcode/line type and value.
        """
        if not isinstance(code, str):
            raise AttributeError("bar_code must be a string")

        code = "".join(char for char in code if char.isdigit())

        valid_length = {47: "line", 44: "bar"}
        if len(code) not in valid_length:
            raise ValueError("code must be 47 digit characters (line) or 44 digit characters (bar)")

        return {"type": valid_length.get(len(code)), "value": code}

    def __get_dv_module_10(self, number: str) -> int:
        """
        - number : str
            The number for which to calculate the module 10 check digit.

        Returns the calculated check digit.
        """
        multipliers = [2, 1] * ((len(number) + 1) // 2)
        total = 0

        for count, digit in enumerate(number[::-1]):
            product = int(digit) * multipliers[count]
            total += product if product < 10 else (product // 10 + product % 10)

        remainder = total % 10
        dv_calculated = (10 - remainder) if remainder != 0 else 0
        return dv_calculated

    def __get_dv_module_11(self, number: str) -> int:
        """
        - number : str
            The number for which to calculate the module 11 check digit.

        Returns the calculated check digit.
        """
        multiplier = 4
        total = 0

        for digit in range(0, len(number)):
            total += int(number[digit]) * multiplier
            multiplier = 10 if multiplier == 2 else multiplier
            multiplier -= 1

        dv = 11 - total % 11

        if dv in {0, 10, 11}:
            return 1

        return dv

    def __get_expiry(self, expiry_factor: str) -> date:
        """
        - expiry_factor : str
            The factor used to calculate the expiry date.

        Returns the calculated expiry date.
        """
        base_date = datetime(1997, 10, 7).date()
        expiry = base_date + timedelta(days=int(expiry_factor))
        return expiry

    def __convert_value_factor(self, value: str) -> float:
        """
        - value : str
            The value factor to convert.

        Returns the converted value into float.
        """
        return float(f"{value[:-2]}.{value[-2:]}")

    def __get_info_from_line(self, line: str) -> Dict[str, Union[str, date, float]]:
        """
        - line : str
            The line string to extract information from.

        Returns a dictionary containing the extracted information.
        """
        match = re.search(r"(\d{3})(\d{1})(\d{6})(\d{11})(\d{11})(\d{1})(\d{4})(\d{10})", line)

        data = {"type": "line",
                "bank": match.group(1),
                "currency": match.group(2),
                "field_1": {"info": match.group(3)[:-1], "dv": match.group(3)[-1]},
                "field_2": {"info": match.group(4)[:-1], "dv": match.group(4)[-1]},
                "field_3": {"info": match.group(5)[:-1], "dv": match.group(5)[-1]},
                "dv": match.group(6),
                "expiry_factor": match.group(7),
                "expiry": self.__get_expiry(match.group(7)),
                "value_factor": match.group(8),
                "value": self.__convert_value_factor(match.group(8))}

        return data

    def __get_info_from_bar(self, bar):
        """
        - bar : str
            The bar string to extract information from.

        Returns a dictionary containing the extracted information.
        """
        match = re.search(r"(\d{3})(\d{1})(\d{1})(\d{4})(\d{10})(\d{5})(\d{10})(\d{10})", bar)

        data = {"type": "bar",
                "bank": match.group(1),
                "currency": match.group(2),
                "dv": match.group(3),
                "expiry_factor": match.group(4),
                "expiry": self.__get_expiry(match.group(4)),
                "value_factor": match.group(5),
                "value": self.__convert_value_factor(match.group(5)),
                "field_1": {"info": match.group(6), "dv": self.__get_dv_module_10(f"{match.group(1)}{match.group(2)}{match.group(6)}")},
                "field_2": {"info": match.group(7), "dv": self.__get_dv_module_10(f"{match.group(7)}")},
                "field_3": {"info": match.group(8), "dv": self.__get_dv_module_10(f"{match.group(8)}")}}

        return data

    def __get_info_from_code(self, code: str) -> Dict[str, Union[str, float, date]]:
        """
        - code : str
            The bar/line code.

        Returns a dictionary containing the extracted information.
        """
        getters = {"line": self.__get_info_from_line, "bar": self.__get_info_from_bar}
        return getters.get(code["type"])(code["value"])

    def get_code_info(self) -> Dict[str, Union[str, float, date]]:
        """
        Returns a dictionary containing the extracted information form line/bar.
        """
        return self.__code_info

    def get_bar(self) -> str:
        """
        Returns the barcode string representation.
        """
        return (f"{self.__code_info['bank']}"
                f"{self.__code_info['currency']}"
                f"{self.__code_info['dv']}"
                f"{self.__code_info['expiry_factor']}"
                f"{self.__code_info['value_factor']}"
                f"{self.__code_info['field_1']['info']}"
                f"{self.__code_info['field_2']['info']}"
                f"{self.__code_info['field_3']['info']}")

    def get_line(self, formatted=False):
        """
        - formatted : bool, optional
            If True, returns the formatted line string.

        Returns the line string representation.
        """
        if formatted:
            return (f"{self.__code_info['bank']}"
                    f"{self.__code_info['currency']}"
                    f"{self.__code_info['field_1']['info'][:1]}"
                    "."
                    f"{self.__code_info['field_1']['info'][1:]}"
                    f"{self.__code_info['field_1']['dv']}"
                    " "
                    f"{self.__code_info['field_2']['info'][:5]}.{self.__code_info['field_2']['info'][5:]}"
                    f"{self.__code_info['field_2']['dv']}"
                    " "
                    f"{self.__code_info['field_3']['info'][:5]}.{self.__code_info['field_3']['info'][5:]}"
                    f"{self.__code_info['field_3']['dv']}"
                    " "
                    f"{self.__code_info['dv']}"
                    " "
                    f"{self.__code_info['expiry_factor']}"
                    f"{self.__code_info['value_factor']}")

        return (f"{self.__code_info['bank']}"
                f"{self.__code_info['currency']}"
                f"{self.__code_info['field_1']['info']}"
                f"{self.__code_info['field_1']['dv']}"
                f"{self.__code_info['field_2']['info']}"
                f"{self.__code_info['field_2']['dv']}"
                f"{self.__code_info['field_3']['info']}"
                f"{self.__code_info['field_3']['dv']}"
                f"{self.__code_info['dv']}"
                f"{self.__code_info['expiry_factor']}"
                f"{self.__code_info['value_factor']}")

    def validate(self):
        """
        Validates the bar/line.

        Returns True if the bar/line is valid, False otherwise.
        """
        dv1_string = f"{self.__code_info['bank']}{self.__code_info['currency']}{self.__code_info['field_1']['info']}"
        dv1_is_valid = self.__get_dv_module_10(dv1_string) == int(self.__code_info['field_1']['dv'])
        dv2_is_valid = self.__get_dv_module_10(f"{self.__code_info['field_2']['info']}") == int(self.__code_info['field_2']['dv'])
        dv3_is_valid = self.__get_dv_module_10(f"{self.__code_info['field_3']['info']}") == int(self.__code_info['field_3']['dv'])

        bar = self.get_bar()
        dv_line_is_valid = self.__get_dv_module_11(f"{bar[:4]}{bar[5:]}") == int(self.__code_info["dv"])

        if not all([dv1_is_valid, dv2_is_valid, dv3_is_valid, dv_line_is_valid]):
            return False

        return True
