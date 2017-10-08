"""Utilities functions file"""
import json
import re

def load_json(filename: str):
    """Loads a json file"""
    with open(filename, encoding="utf-8", mode="r") as file:
        data = json.load(file)
    return data

def save_json(data: json, filename: str, should_be_sorted=True):
    """Saves a json file"""
    with open(filename, encoding="utf-8", mode="w") as file:
        json.dump(data, file, indent=4, sort_keys=should_be_sorted, separators=(',', ': '))


def convert_seconds_to_str(sec: float):
    """Returns a str representing a number of seconds"""
    msg = ""
    sec = round(sec)
    years = sec // 31536000
    if years != 0:
        msg += str(int(years)) + "y "
    sec -= years * 31536000
    days = sec // 86400
    if days != 0:
        msg += str(int(days)) + "d "
    sec -= days * 86400
    hours = sec // 3600
    if hours != 0:
        msg += str(int(hours)) + "h "
    sec -= hours * 3600
    minutes = sec // 60
    sec -= minutes * 60
    if minutes != 0:
        msg += str(int(minutes)) + "m "
    if sec != 0:
        msg += str(int(sec)) + "s "
    return msg[:-1]


SECONDS_VALUES = [31536000, 86400, 3600, 60, 1]

def convert_str_to_seconds(duration: str):
    """Converts a duration (format %Yy %dd %Hh %Mm %Ss) to the total
       number of corresponding seconds.

       If the format of duration isn't correct, returns -1."""
    regex = re.compile("(?=.*[ydhms])( *[0-9]+y *)?( *[0-9]+d *)?( *[0-9]+h *)?( *[0-9]+m *)?( *[0-9]+s *)?") #pylint: disable=line-too-long

    if not regex.fullmatch(duration):
        return -1

    total_seconds = 0
    matches = regex.findall(duration)
    for i in range(5):
        match = matches[0][i]
        if match != "":
            end_of_match = match.find(" ") - 1 if match.find(" ") != -1 else len(match) - 1
            value = int(match[:end_of_match])
            total_seconds += SECONDS_VALUES[i] * value
    return total_seconds


def convert_int_to_str(number: int, char: str = "'"):
    """Converts an ugly int into a beautiful and sweet str

    Parameters:
        nb: The number which is gonna be converted.
        char: The characters which are gonna be inserted between every 3 digits.

    Example: 2364735247 --> 2'364'735'247"""
    number = str(number)
    for index in range(len(number) - 3, 0, -3):
        number = number[:index] + char + number[index:]
    return number
