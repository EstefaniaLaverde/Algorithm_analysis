# Escoger arbitrariamente un eje, incluir el vértice de mayor grado de los dos vértices conectados por el eje, descartar todos los demás ejes conectados por el vértice escogido y repetir hasta que no queden ejes.
import random

def solve(edges: list) -> list:
    sol = []
    
    # almacenar los ejes en un set para eliminacion O(1)
    edge_set = {tuple(sorted(edge)) for edge in edges}
    
    neighbours = {}
    degrees = {}
    for u, v in edge_set:
        neighbours.setdefault(u, set()).add(v)
        neighbours.setdefault(v, set()).add(u)
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    
    while edge_set:
        edge = edge_set.pop()
        u, v = edge
        
        if degrees[u] >= degrees[v]:
            chosen = u
        else:
            chosen = v
        
        sol.append(chosen)
        
        for neighbour in list(neighbours.get(chosen, [])):
            edge_neigh = tuple(sorted((chosen, neighbour)))
            edge_set.discard(edge_neigh)
            
            neighbours[neighbour].discard(chosen)
            degrees[neighbour] -= 1
        
        neighbours[chosen].clear()
        degrees[chosen] = -1
    
    return sol

# Ejemplo de uso:
# edges = [(1, 2), (2, 3), (3, 4), (2, 4), (2, 5)]
# print(solve(edges))
