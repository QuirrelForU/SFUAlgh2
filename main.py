"""
Savelev Aleksandr КИ22-16\1б
Variant 5 Boyer-Moore-Horspool algorithm
"""
import argparse
import hashlib
import time
from typing import Dict, Union, Callable, Any
from colorama import init
from search import search


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator to measure and log the execution time of a function.

    Args:
        func (callable): The function to be measured.

    Returns:
        callable: A wrapped function that logs the execution time.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        return result

    return wrapper


def find_key_by_value(dictionary: Dict[str, Union[tuple, None]], target_value: int) -> str | None:
    """
    Find a key in a dictionary by its associated value.

    Args:
        dictionary (dict): The input dictionary to search in.
        target_value (int): The value to search for.

    Returns:
        str | None: The key corresponding to the target_value, or None if not found.
    """
    for key, value in dictionary.items():
        if value is not None and target_value in value:
            return key
    return None


@timer
def main():
    """
    Main function for using the search method that uses the Boyer-Moore-Horspool algorithm in the terminal.
    This function reads user input, searches for substrings in a text file, and provides colored output.
    Args: None
    Returns: None
    """
    init()
    parser = argparse.ArgumentParser(description="Search for substrings in a text file with colored output.")
    parser.add_argument("file_path", help="Path to the file where the search will be performed.")
    parser.add_argument("search_strings", nargs='+', help="One or more search strings.")
    parser.add_argument("--case-sensitive", action="store_true", help="Perform a case-sensitive search.")
    parser.add_argument("--method", choices=["first", "last"], default="first",
                        help="Search method: 'first' or 'last'. Default is 'first'.")
    parser.add_argument("--count", type=int, help="Maximum number of matches to return. Default is None (all).")
    parser.add_argument("--color-output", action="store_true", help="Perform additional color output in  terminal.")

    args = parser.parse_args()

    with open(args.file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    search_strings = args.search_strings
    case_sensitivity = args.case_sensitive
    method = args.method
    count = args.count
    color_output = args.color_output

    result = search(text, search_strings, case_sensitivity, method, count)
    formatted_output = ""
    for key, value in result.items():
        formatted_output += f"{key}: {value}\n"

    print(formatted_output)

    if result and color_output:
        colored_text = ''
        previous_last = 0
        filtered_dict = {key: value for key, value in result.items() if value is not None}
        flattened_list = sorted([item for tup in filtered_dict.values() for item in tup])
        for pos in flattened_list:
            key = find_key_by_value(filtered_dict, pos)
            seed = int(hashlib.sha256(key.encode()).hexdigest(), 16)
            color_number = seed % 6 + 31
            if pos >= previous_last:
                colored_text += text[previous_last:pos] + f'\033[{color_number}m' + text[
                                                                                    pos:pos + len(key)] + '\033[39m'
                previous_last = pos + len(key)

        print(colored_text[flattened_list[0]:flattened_list[0] + 500] + '\033[39m')
#

if __name__ == "__main__":
    main()
