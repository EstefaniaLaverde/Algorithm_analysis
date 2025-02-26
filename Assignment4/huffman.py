import heapq
import math
import sys


def print_codification_report(text,codification):
    #hacer prints con reportes de la codificacion
    #la codificacion
    #numero de bits esperado
    #entropia en el peor de los casos
    #numero total de bits para el texto comprimodo

    counts = {}
    for char in text:
        if char not in counts:
            counts[char] = 0
        counts[char] += 1

    print('codification:')
    print(sorted(list(codification.items())))

    text_len=sum(counts.values())


    expected_bit_count=0
    for c,count in counts.items():
        expected_bit_count+=(count/text_len)*len(codification[c])
    print('expected bit count per character:',expected_bit_count)


    print('worst case entropy:',math.log2(len(counts)))


    total_bits_compr=0
    for c,count in counts.items():
        total_bits_compr+=count*len(codification[c])

    print('total bits on compressed file:',total_bits_compr)

class Node:
    """Se construye el arbol binario usando la cola de prioridad y la clase node. """
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



def get_huffman_codes(root):
    """ Determinar los codigos de huffman recorriendo el arbol binario resultante y asignando 0 o 1 a los arcos"""
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



def encode_text(text, codification):
    encoded = ""
    for char in text:
        if char in codification:
            encoded += codification[char]
        else:
            raise ValueError(f"Character '{char}' not found in codification mapping.")
    return encoded



if __name__=='__main__':
    input_file=sys.argv[1]
    output_file=sys.argv[2]

    with open(input_file) as f:
        text=f.read()
    
    tree = huffman(text)
    codification=get_huffman_codes(tree)
    cod_text = encode_text(text,codification)
    print_codification_report(text,codification)

    with open(output_file,'w') as f:
        f.write(cod_text)