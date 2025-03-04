def build_suffix_array(text: str) -> list[int]:
    return sorted(range(len(text)), key=lambda i: text[i:])

def print_suffix_array(text: str, suffix_array: list[int]) -> None:
    print([text[index:] for index in suffix_array])

def binary_search_substring(text: str, suffix_array: list[int], substring: str) -> tuple[int, int]:
    # Buscar primera ocurrencia
    left, right = 0, len(suffix_array)
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:]
        if suffix.startswith(substring):
            right = mid
        elif suffix < substring:
            left = mid + 1
        else:
            right = mid
    first = left

    # Buscar última ocurrencia
    left, right = first, len(suffix_array)
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:]
        if suffix.startswith(substring):
            left = mid + 1
        else:
            right = mid
    last = left

    return sorted(suffix_array[first:last])

text = 'banana$'
suff_arr = build_suffix_array(text)
print("Sufijos ordenados:")
print_suffix_array(text, suff_arr)
ocurrences = binary_search_substring(text, suff_arr, 'a')
print(ocurrences)