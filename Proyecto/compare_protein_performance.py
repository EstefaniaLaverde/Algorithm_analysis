
from protein_dataset.read_protein_dataset import load_protein_dataset

import networkx as nx
import my_vf2pp
import algoritmo_genetico
import vf2pp_fingerprints
import backtracking_y_fingerprint

from backtracking_y_fingerprint import graficar_grafo

import time

import pandas as pd

import itertools

from copy import deepcopy

graphs=load_protein_dataset('protein_dataset/truncated_dataset.txt')
# graphs = load_protein_dataset('biological_datasets/truncated_mutag.txt')

datos=pd.DataFrame(columns=['algorithm','S_n_nodes','S_n_edges','G_n_nodes','G_n_edges','time','found_mapping'])

times_vf2pp_nx = []
times_vf2pp = []
times_backtracking = []

# print(graphs)
for S,G in itertools.permutations(graphs,2):
    # print('label values are subset',set(S[1].values()).issubset(set(G[1].values())))
    # print('S valid nodes',set(itertools.chain.from_iterable(S[0]))==set(S[1].keys()))
    # print('G valid nodes',set(itertools.chain.from_iterable(G[0]))==set(G[1].keys()))

    #-------------------------------
    #sacar datos de networkx

    try:
        start=time.time()
        S_nx=nx.Graph()
        S_nx.add_edges_from(S[0])

        G_nx=nx.Graph()
        G_nx.add_edges_from(G[0])

        #toca hacer algo para poder meterle labels a networkx

        GM=nx.algorithms.isomorphism.GraphMatcher(G_nx,S_nx)
        ans=GM.subgraph_is_isomorphic()
        # ansnx = None
        # if ans == True:
        #     ansnx = ans
        #     mapping = GM.mapping
        #     print('G',G)
        #     print('S',S)

        end=time.time()
        resultados=pd.DataFrame([['nx_vf2++',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans]],columns=datos.columns)
        times_vf2pp_nx.append(end-start)
        datos=pd.concat((datos,resultados),ignore_index=True)
    except:
        pass
    #---------------------------------------------
    #sacar datos de my_vf2pp
    start=time.time()
    G_own=my_vf2pp.graph(list(G[1].keys()),G[0],G[1])
    S_own=my_vf2pp.graph(list(S[1].keys()),S[0],S[1])

    ans=(len(my_vf2pp.vf2pp(S_own,G_own))==len(S_own.nodes))

    end=time.time()
    resultados=pd.DataFrame([['our_vf2++',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans]],columns=datos.columns)

    datos=pd.concat((datos,resultados),ignore_index=True)
    times_vf2pp.append(end-start)
    #-------------------------------------------
    #sacar datos de algoritmo genetico

    

    #-----------------------

    #sacar datos de backtracking y fingerprints
    start = time.time()
    G_own=my_vf2pp.graph(list(G[1].keys()),G[0],G[1])
    S_own=my_vf2pp.graph(list(S[1].keys()),S[0],S[1])
    solver = backtracking_y_fingerprint.BacktrackingFingerprintIsomorphismSolver(S_own, G_own)
    ans = solver.calcular_isomorfismo_backtracking()
    end = time.time()
    resultados=pd.DataFrame([['fingerprints and backtracking',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans != {}]],columns=datos.columns)
    datos=pd.concat((datos,resultados),ignore_index=True)
    times_backtracking.append(end-start)



print(datos.to_markdown())

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Crear DataFrame
data = pd.DataFrame({
    "Tiempo (s)": times_vf2pp_nx + times_vf2pp + times_backtracking,
    "Algoritmo": ["VF2++ NetworkX"]*len(times_vf2pp_nx) + 
                 ["VF2++ Personalizado"]*len(times_vf2pp) + 
                 ["Backtracking"]*len(times_backtracking),
    "Ejecución": list(range(len(times_vf2pp_nx))) + 
                 list(range(len(times_vf2pp))) + 
                 list(range(len(times_backtracking)))
})

# Gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=data,
    x="Ejecución",
    y="Tiempo (s)",
    hue="Algoritmo",
    style="Algoritmo",
    markers=True,  # Puntos en cada dato
    dashes=False,  # Líneas continuas
    linewidth=2,
    palette="tab10"
)

plt.title("Comparación de Tiempos por Ejecución")
plt.xlabel("Número de Ejecución")
plt.ylabel("Tiempo (segundos)")
plt.legend(title="Algoritmo", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
