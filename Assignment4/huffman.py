import heapq

class Node:
    def __init__(self, freq=0, char=None):
        self.char = char
        self.left = None
        self.right = None
        self.freq = freq

    def add_left(self, node):
        self.left = node
        self.freq += node.freq

    def add_right(self, node):
        self.right = node
        self.freq += node.freq

    # cuando la min queue compara dos elementos por freq (y hay un empate) procede a comparar con esto (arbitrariamente)
    def __lt__(self, other):
        return self.freq < other.freq

def get_ordered_frequencies(text):
    counts = {}
    for char in text:
        if char not in counts:
            counts[char] = 0
        counts[char] += 1

    freqs = []
    text_size = len(text)
    for char, count in counts.items():
        n = Node(count / text_size, char)
        freqs.append((count / text_size, n))
    heapq.heapify(freqs)
    
    return freqs

def huffman(text):
    # implementacion de huffman encoding con min heap (frequency, node)
    Q = get_ordered_frequencies(text)

    while len(Q) > 1:
        z = Node()
        z.add_left(heapq.heappop(Q)[1])
        z.add_right(heapq.heappop(Q)[1])
        heapq.heappush(Q, (z.freq, z))
    return Q[0][1] if Q else None


def visualize_tree(root, level=0, prefix="Root: "):
    if root is None:
        return
    
    indent = "__" * level
    
    if root.char is not None:
        print(f"{indent}{prefix}'{root.char}' (freq: {root.freq:.2f})")
    else:
        print(f"{indent}{prefix}Node (freq: {root.freq:.2f})")
    
    if root.left:
        visualize_tree(root.left, level + 1, "L: ")
    if root.right:
        visualize_tree(root.right, level + 1, "R: ")


def get_huffman_codes(root):
    codes = {}

    def traverse(node, current_code=""):
        if node.char is not None:
            codes[node.char] = current_code if current_code else "0"
            return
        
        if node.left:
            traverse(node.left, current_code + "0")
        
        if node.right:
            traverse(node.right, current_code + "1")
    
    traverse(root)
    return codes


text = "aabbcddddddddd"
tree = huffman(text)
# visualizacion
print("Huffman Tree:")
visualize_tree(tree)
print('')
# codigos
codes = get_huffman_codes(tree)
print("Huffman Codes:")
for char, code in codes.items():
    print(f"'{char}': {code}")
