from typing import Union, Optional


def foo() -> None:
    print('zalupa')


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity=False,
           method: str = 'first', count: Optional[int] = None) -> Optional[
    Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, str):
            sub_string = sub_string.lower()
        elif isinstance(sub_string, list):
            sub_string = [s.lower() for s in sub_string]

    def boyer_moore_horspool(text, pattern):
        m, n = len(pattern), len(text)
        if m == 0 or m > n:
            return []

        last_occurrence = {}
        for i in range(m - 1):
            last_occurrence[pattern[i]] = m - i - 1

        result = []
        i = m - 1
        while i < n:
            k = 0
            j = i
            while k < m and pattern[m - 1 - k] == text[j]:
                k += 1
                j -= 1
            if k == m:
                result.append(i - m + 1)
                if method == 'first' and count is not None and len(result) >= count:
                    break
                i += 1
            else:
                if text[i] in last_occurrence:
                    i += last_occurrence[text[i]]
                else:
                    i += m

        return result

    if isinstance(sub_string, str):
        positions = boyer_moore_horspool(string, sub_string)
    elif isinstance(sub_string, list):
        positions = {sub: boyer_moore_horspool(string, sub) for sub in sub_string}

    if method == 'last':
        if isinstance(positions, list):
            positions = positions[::-1]
        elif isinstance(positions, dict):
            positions = {sub: pos[::-1] for sub, pos in positions.items()}

    if count is not None:
        if isinstance(positions, list):
            positions = positions[:count]
        elif isinstance(positions, dict):
            positions = {sub: pos[:count] for sub, pos in positions.items()}

    return positions


test = "Hello, world! Hello, Universe! Hello, everyone!"
print(search(test, ["Hello", "everyone"]))
