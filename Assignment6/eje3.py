import random

def solve(edges: list) -> list:
    """
    Esta función resuelve el problema de encontrar un conjunto de nodos que cubren todas las aristas de un grafo.
    Utiliza un algoritmo de selección de nodos basado en escoger arbitrariamente un eje, incluir el vértice de mayor grado de los dos vértices conectados por el eje, descartar todos los demás ejes conectados por el vértice escogido y repetir hasta que no queden ejes.
    
    Parámetros:
    edges (list): Una lista de aristas del grafo, representadas como tuplas de dos enteros.
    
    Retorna:
    list: Un conjunto de nodos que cubren todas las aristas del grafo.
    """
    sol = []
    
    # Convertir los ejes a un set para permitir eliminaciones O(1)
    edge_set = {tuple(sorted(edge)) for edge in edges}
    
    # Inicializar diccionarios para vecinos y grados
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
        
        # Seleccionar el vértice de mayor grado
        if degrees[u] >= degrees[v]:
            chosen = u
        else:
            chosen = v
        
        sol.append(chosen)
        
        # Eliminar todos los ejes conectados al vértice seleccionado
        for neighbour in list(neighbours.get(chosen, [])):
            edge_neigh = tuple(sorted((chosen, neighbour)))
            edge_set.discard(edge_neigh)
            
            # Eliminar el vértice seleccionado de los vecinos
            neighbours[neighbour].discard(chosen)
            # Decrementar el grado de los vecinos
            degrees[neighbour] -= 1
        
        # Limpiar los vecinos del vértice seleccionado y marcar su grado como -1
        neighbours[chosen].clear()
        degrees[chosen] = -1
    
    return sol
