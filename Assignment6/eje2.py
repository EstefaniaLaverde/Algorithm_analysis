import heapq

class updatable_heap:
    def __init__(self,values):
        self.values=values
        heapq.heapify(self.values)
        self.values_pos={val:i for i,val in enumerate(self.values)}

def solve(edges: list[tuple]) -> list:
    """
    Esta función resuelve el problema de encontrar un conjunto de nodos que cubren todas las aristas de un grafo.
    Utiliza un algoritmo de selección de nodos basado en el grado de los nodos, seleccionando siempre el nodo de mayor grado disponible.
    
    Parámetros:
    edges (list): Una lista de aristas del grafo, representadas como tuplas de dos enteros.
    
    Retorna:
    list: Un conjunto de nodos que cubren todas las aristas del grafo.
    """
    neighs={}

    #ordernar cordenadas de los edges para representacion canonica
    edges=map(lambda x: tuple(sorted(x)), edges)
    #edges es un set para despues quitarle elementos facilmente
    edges=set(edges)


    max_degree=0

    #crear conjuntos de vecinos
    for u,v in edges:
        if u not in neighs:
            neighs[u]=set()
        neighs[u].add(v)

        if v not in neighs:
            neighs[v]=set()
        neighs[v].add(u)

        max_degree=max(max_degree,len(neighs[u]))
        max_degree=max(max_degree,len(neighs[v]))


    buckets=[set() for i in range(max_degree+1)]

    #agrupoar nodos en buckets segun su grado
    for node in neighs:
        buckets[len(neighs[node])].add(node)

    cover=[]
    #recorrer en orden inverso los buckets, para seleccionar siempre un nodo de grado maximo
    for i in range(max_degree,0,-1):
        while len(buckets[i]):
            node=buckets[i].pop()
            cover.append(node)

            #cambiar de bucket los vecinos del nodo
            for neigh in neighs[node]:
                neigh_degree=len(neighs[neigh])
                buckets[neigh_degree].remove(neigh)
                buckets[neigh_degree-1].add(neigh)

            #remover ejes relacionados a node
            for neigh in neighs[node]:
                neighs[neigh].remove(node)

            neighs[node].clear()

    return cover