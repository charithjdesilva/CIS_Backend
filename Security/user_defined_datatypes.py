import re

class SriLankaMobileNumber:
    def __init__(self, number):
        self.number = self.clean_number(number)

    def clean_number(self, number):
        # Remove non-digit characters, leading '+' if present, and leading '0' if present
        cleaned_number = re.sub(r'\D', '', number)
        if cleaned_number.startswith('0'):
            cleaned_number = cleaned_number[1:]
        if cleaned_number.startswith('94'):
            cleaned_number = cleaned_number[2:]
        return cleaned_number

    def format(self):
        # Format the number as 0xx-xxxxxxx
        formatted_number = self.number
        if len(formatted_number) == 9:
            formatted_number = '0' + formatted_number[:2] + '-' + formatted_number[2:]
        return formatted_number

    def is_valid(self):
        # Check if the number is a valid Sri Lanka mobile number (9 digits)
        return len(self.number) == 9

    def __str__(self):
        return self.format()
