import sys
import numpy as np

def solution_matrix(nodes, edges, k=6):
    #diccionario de reenumeracion de nodos para matriz de adyacencia
    node_to_ind = {node: i for i, node in enumerate(nodes)}
    A = np.eye(len(nodes))

    for x, y in edges:
        A[node_to_ind[x], node_to_ind[y]] = 1
        A[node_to_ind[y], node_to_ind[x]] = 1

    A_k = np.linalg.matrix_power(A, k)

    return A_k.min() > 1/2

if __name__ == '__main__':

    # Guardar resultados
    results = []

    with open(sys.argv[1]) as f:
        content = f.read()
        sections = [section.strip() for section in content.split('\n\n') if section.strip()]

    for section in sections:
        lines = section.splitlines()  
        nodes = list(map(int, lines[0].split()))
        m = int(lines[1])
        edges = []
        for i in range(2, 2 + m):
            a, b = map(int, lines[i].split())
            edges.append((a, b))

        result = solution_matrix(nodes, edges)
        results.append(result)
        print(result)

    with open(sys.argv[2], 'w') as f:
        for result in results:
            f.write(str(result) + '\n')
