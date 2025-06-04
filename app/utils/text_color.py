'''
This module is used to style text color within CLI.
'''

def green(text:str) -> str:
    return f"\033[32m{text}\033[0m"

def blue(text:str) -> str:
    return f"\033[38;5;117m{text}\033[0m"
