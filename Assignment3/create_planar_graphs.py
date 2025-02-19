import networkx as nx
import pandas as pd
import random
import itertools

def create_random_graph(num_vertices:int, file_name:str) -> None:
    """
    Crea un grafo planar aleatorio con un número específico de vértices.
    
    El algoritmo inicia con un triángulo y va añadiendo vértices de forma iterativa,
    conectando cada nuevo vértice a los tres vértices de un triángulo existente elegido al azar. Este proceso garantiza que el grafo resultante sea planar.
    
    Args:
        num_vertices (int): Número de vértices que tendrá el grafo. Debe ser >= 3.
        file_name (str): Nombre del archivo CSV donde se guardará el grafo.
                        El archivo tendrá dos columnas: 'source' y 'target' 
                        representando los extremos de cada arista.
    
    Returns:
        None: El grafo se guarda en un archivo CSV.
    """
    
    triangles = [(1,2,3)]
    vertices = [1,2,3]

    while len(vertices) < num_vertices:
        triangle = random.choice(triangles)
        combinaciones = list(itertools.combinations(triangle, 2)) 

        # print(f'vertex f{len(vertices)+1} was added to triangle {triangle}')
        combinaciones = [comb+(len(vertices)+1,) for comb in combinaciones]
        triangles.remove(triangle)
        triangles += combinaciones 
        vertices.append(len(vertices)+1)


    edges = set()
    for tup in triangles:
        edges.update({(tup[i], tup[j]) for i in range(len(tup)) for j in range(i + 1, len(tup))})
    
    df = pd.DataFrame(list(edges), columns=['source', 'target'])
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    # crear grafo 
    create_random_graph(20, 'grafo1.csv')

