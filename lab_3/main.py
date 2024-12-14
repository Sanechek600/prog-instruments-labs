import csv
import json
import re
from typing import Any, Dict, List

import checksum


patterns: Dict[str, str] = {
    "telephone": r"^\+7\-\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$",
    "height": r"^(1\.[4-9]\d|2\.[0-4]\d|2\.50)$",
    "inn": r"^\d{12}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",
    "occupation": r"^[A-Za-zА-Яа-яёЁ\s-]+$",
    "latitude": r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$",
    "blood type": r"^(A|B|AB|O)[\u2212+]$",
    "issn": r"^\d{4}-\d{4}$",
    "uuid": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
    "date": r"^(?:19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
}

def row_check(row: List[str]) -> bool:
    """
    Checks a string for compliance with the patterns.
    Args:
        row: List of row values.
    Returns:
        True if an error was found, False otherwise.
    """
    for i in range(10):
        if not re.match(patterns[i], row[i]):
            return False
    return True

def process_csv(file_path: str) -> List[int]:
    """
    Checks all rows in a .csv file to find rows that do not
    match the designated patterns
    Args:
        file_path: path to the .csv file
    Returns:
        List of invalid rows
    """
    invalid_rows = []
    with open(file_path, mode='r', newline='', encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for i, row in enumerate(reader, start=0):
            if not row_check(row):
                invalid_rows.append(i)
    return invalid_rows