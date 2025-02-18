import networkx as nx
import pandas as pd
import random
import itertools

def create_random_graph(num_vertices:int, file_name:str) -> None:
    #TODO: comentar la funcion
    triangles = [(1,2,3)]
    vertices = [1,2,3]

    while len(vertices) < num_vertices:
        triangle = random.choice(triangles)
        combinaciones = list(itertools.combinations(triangle, 2)) 

        print(f'vertex f{len(vertices)+1} was added to triangle {triangle}')
        combinaciones = [comb+(len(vertices)+1,) for comb in combinaciones]
        triangles.remove(triangle)
        triangles += combinaciones 
        vertices.append(len(vertices)+1)


    edges = set()
    for tup in triangles:
        edges.update({(tup[i], tup[j]) for i in range(len(tup)) for j in range(i + 1, len(tup))})
    
    df = pd.DataFrame(list(edges), columns=['source', 'target'])
    df.to_csv(file_name, index=False)


create_random_graph(20, 'graphs/grafo1.csv')
