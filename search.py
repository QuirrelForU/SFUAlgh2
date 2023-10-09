from typing import Union, Optional


def foo() -> None:
    print('zalupa')


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity=False,
           method: str = 'first', count: Optional[int] = None) -> Optional[
    Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    '''
    pass
    :param string:
    :param sub_string:
    :param case_sensitivity:
    :param method:
    :param count:
    :return:
    '''

    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, str):
            sub_string = sub_string.lower()
        elif isinstance(sub_string, tuple):
            sub_string = tuple([s.lower() for s in sub_string])

    def boyer_moore_horspool(text: object, pattern: object) -> object:
        if method == 'first':
            m, n = len(pattern), len(text)
            if m == 0 or m > n:
                return None
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
                    if count is not None and len(result) >= count:
                        break
                    i += 1
                else:
                    if text[i] in last_occurrence:
                        i += last_occurrence[text[i]]
                    else:
                        i += m
        else:
            pattern = pattern[::-1]
            m, n = len(pattern), len(text)
            if m == 0 or m > n:
                return None
            last_occurrence = {}
            for i in range(m - 1):
                last_occurrence[pattern[i]] = m - i - 1
            result = []
            i = len(text) - m
            while i >= 0:
                k = 0
                j = i
                while k < m and pattern[m - 1 - k] == text[j]:
                    k += 1
                    j += 1
                if k == m:
                    result.append(i)
                    if count is not None and len(result) == count:
                        break
                    i -= 1
                else:
                    if text[i] in last_occurrence:
                        i -= last_occurrence[text[i]]
                    else:
                        i -= m
        if not result:
            return None
        return tuple(result)

    positions = dict()
    if isinstance(sub_string, str):
        positions = boyer_moore_horspool(string, sub_string)
    elif isinstance(sub_string, tuple):
        positions = {sub: boyer_moore_horspool(string, sub) for sub in sub_string}
        flattened_list = [item for tup in positions.values() for item in tup]
        if count is not None:
            flattened_list = sorted(flattened_list)[:count]
            for key, value in positions.items():
                value = tuple(elem for elem in value if elem in flattened_list)
                positions[key] = value
        if set(positions.values()) == {None}:
            positions = None

    return positions

print(search('', ('abc', 'a'), False, 'first', 1))
#Иправить ошибку при 'abc': None
