import sys

# busqueda binaria
def search(pat, text, suffArr):
    n=len(text)
    m = len(pat)
    l = 0
    r = n-1

    while l <= r:
        mid = l + (r - l)//2
        substring = text[suffArr[mid]:suffArr[mid]+m]
        print(f'indices: {suffArr[mid],suffArr[mid]+m}; substring: {substring}')

        if substring == pat:
            return suffArr[mid]

        if substring < pat:
            l = mid + 1
        else:
            r = mid - 1

    return None
	
# construir arreglo de sufijos
def buildSuffixArray(text):
    n=len(text)
    suffixes = [text[i:] for i in range(n)]
    suffixes.sort()
    suffArr = [text.index(suff) for suff in suffixes]

    return suffArr



text = "ensayo"
pat = "ay" 
suffArr = buildSuffixArray(text)

index = search(pat, text, suffArr)

print(f'index: {index}')

