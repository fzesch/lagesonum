# coding: utf-8

# TODO: refactor: create one function "validate" for general validation, easier for external calling
import re

MALICIOUS_EXPRESSIONS = ["DROP", "TABLE", "DELETE"]

# default parameters for checking validity of number
LAGESO_pattern = re.compile("^[a-zA-Z][0-9]+$")
LAGESO_min = 0
LAGESO_max = 99


# TODO: fetch validation pattern, min and max from database, based on location argument (for multi-location scalability)
def is_valid_number(number, pattern=LAGESO_pattern):
    """
    Checks, whether a number is in a valid format for a pattern given for a location
    To be run before insertion into db
    :param number: number to be checked
    :param pattern: regular expression
    :return: boolean
    """
    if re.findall(pattern, number):
        return not any(map(lambda expr: expr in number, MALICIOUS_EXPRESSIONS))
    else:
        return False
