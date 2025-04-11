def solve(edges:list[tuple]) -> list:
    """
    Resuelve el problema de cubrimiento de vértices en un grafo con el siguiente algoritmo:
    Escoger arbitrariamente un eje, incluir los dos vértices conectados, descartar todos los demás ejes conectados por los vertices escogidos y repetir hasta que no queden ejes.
    
    Parameters:
    edges (list): Una lista de pares de vértices que representan las aristas del grafo.
    
    Returns:
    list: Una lista de vértices que cubren todas las aristas del grafo.
    """
    neighs={}

    # Ordenar las coordenadas de los edges para representación canónica
    edges=map(lambda x: tuple(sorted(x)), edges)
    # Convertir edges a un set para poder quitar elementos fácilmente
    edges=set(edges)

    # Crear conjuntos de vecinos
    for u,v in edges:
        if u not in neighs:
            neighs[u]=set()
        neighs[u].add(v)

        if v not in neighs:
            neighs[v]=set()
        neighs[v].add(u)

    cover=[]

    while len(edges):
        # Obtener un edge arbitrario
        u,v=edges.pop()

        # Agregar nodos del edge al cover
        cover.append(u)
        cover.append(v)

        # Quitar edges que usan a u
        for neigh in neighs[u]:
            edge=tuple(sorted((u,neigh)))
            if edge in edges:
                edges.remove(edge)
            neighs[neigh].remove(u)
        neighs[u].clear()

        # Quitar edges que usan a v
        for neigh in neighs[v]:
            edge=tuple(sorted((v,neigh)))
            if edge in edges:
                edges.remove(edge)
            neighs[neigh].remove(v)
        neighs[v].clear()

    return cover



        


        