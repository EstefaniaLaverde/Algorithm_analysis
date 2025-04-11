import random
import time
import pandas as pd
from eje1 import solve as solve1
from eje2 import solve as solve2
from eje3 import solve as solve3
from eje4 import solve as solve4

def generar_grafo_aleatorio(num_vertices, num_aristas):
    # Grafos sin loops o multiejes
    if num_aristas > (num_vertices * (num_vertices - 1)) // 2:
        num_aristas = (num_vertices * (num_vertices - 1)) // 2 

    edges = set()
    while len(edges) < num_aristas:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v:
            e = tuple(sorted([u, v]))
            edges.add(e)
    return list(edges)

def probar_algoritmos():
    tamanos = [100, 1000, 10000]
    multiplicadores_aristas = [10, 50, 100]

    resultados = []

    algoritmos = [
        ("Alg.1", solve1),
        ("Alg.2", solve2),
        ("Alg.3", solve3),
        ("Alg.4", solve4)
    ]
    
    for n in tamanos:
        for mult in multiplicadores_aristas:
            m = n * mult
            edges = generar_grafo_aleatorio(n, m)
            
            for alg_n, alg_f in algoritmos:

                start = time.time()
                cover = alg_f(edges.copy())
                end = time.time()
                resultados.append({
                    "Vertices": n,
                    "Multiplicador": mult,
                    "Edges": m,
                    "Algorithm": alg_n,
                    "Cover Size": len(cover),
                    "Time (s)": end - start
                })
    
    df = pd.DataFrame(resultados)
    return df

if __name__ == "__main__":
    df = probar_algoritmos()
    print(df.to_markdown(index=False))
