"""
This module provides a search function that uses the Boyer-Moore-Horspool algorithm to find substrings in a string.
"""
from typing import Union, Optional, Tuple


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity=False,
           method: str = 'first', count: Optional[int] = None) -> Optional[
    Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Search for substring(s) in a string using the Boyer-Moore-Horspool algorithm
    :param string: The input string to search in
    :param sub_string: The substring(s) to search for. Can be a string or a list of strings
    :param case_sensitivity: If True, perform a case-sensitive search (default is False)
    :param method: The search method, either 'first' or 'last' (default is 'first')
    :param count: The maximum number of matches to return (default is None, which means all)

    :return: A dictionary containing positions of the found substring(s) in the input string.
             If count is specified, only the first 'count' matches are returned.
    """

    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, str):
            sub_string = sub_string.lower()
        else:
            sub_string = tuple(s.lower() for s in sub_string)

    def boyer_moore_horspool(text: str, pattern: str) -> Tuple[int, ...] | None:
        """
                Search for a single substring in the input text using Boyer-Moore-Horspool algorithm
                :param text: The input text to search in
                :param pattern: The substring to search for
                :return: A tuple of integers representing the positions of matches in the text
         """
        if method == 'first':
            pattern_length, text_length = len(pattern), len(text)
            if pattern_length == 0 or pattern_length > text_length:
                return None
            last_occurrence = {}
            for i in range(pattern_length - 1):
                last_occurrence[pattern[i]] = pattern_length - i - 1

            result = []
            i = pattern_length - 1
            while i < text_length:
                k = 0
                j = i
                while k < pattern_length and pattern[pattern_length - 1 - k] == text[j]:
                    k += 1
                    j -= 1
                if k == pattern_length:
                    result.append(i - pattern_length + 1)
                    if count is not None and len(result) >= count:
                        break
                    i += 1
                else:
                    if text[i] in last_occurrence:
                        i += last_occurrence[text[i]]
                    else:
                        i += pattern_length
        else:
            pattern = pattern[::-1]
            pattern_length, text_length = len(pattern), len(text)
            if pattern_length == 0 or pattern_length > text_length:
                return None
            last_occurrence = {}
            for i in range(pattern_length - 1):
                last_occurrence[pattern[i]] = pattern_length - i - 1
            result = []
            i = len(text) - pattern_length
            while i >= 0:
                k = 0
                j = i
                while k < pattern_length and pattern[pattern_length - 1 - k] == text[j]:
                    k += 1
                    j += 1
                if k == pattern_length:
                    result.append(i)
                    if count is not None and len(result) == count:
                        break
                    i -= 1
                else:
                    if text[i] in last_occurrence:
                        i -= last_occurrence[text[i]]
                    else:
                        i -= pattern_length
        if not result:
            return None
        return tuple(result)

    if isinstance(sub_string, str):
        positions = boyer_moore_horspool(string, sub_string)
    # elif isinstance(sub_string, tuple):
    else:
        positions = {sub: boyer_moore_horspool(string, sub) for sub in sub_string}
        if count is not None:
            filtered_dict = {key: value for key, value in positions.items() if value is not None}
            flattened_list = [item for tup in filtered_dict.values() for item in tup]
            if method == 'first':
                flattened_list = sorted(flattened_list)[:count]
            else:
                flattened_list = sorted(flattened_list, reverse=True)[:count]
            for key, value in filtered_dict.items():
                value = tuple(elem for elem in value if elem in flattened_list)
                if value:
                    positions[key] = value
                else:
                    positions[key] = None
        if set(positions.values()) == {None}:
            positions = None

    return positions
