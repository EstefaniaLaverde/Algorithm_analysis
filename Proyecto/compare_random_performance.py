# Read dataset
from protein_dataset.read_protein_dataset import load_protein_dataset
# Networkx vf2 algorithm
from networkx.algorithms import isomorphism
import networkx as nx

# vf2++ implementation
import my_vf2pp

# Proposed algorithm
import backtracking_y_fingerprint

# Other libraries
import pandas as pd
import tracemalloc
import itertools
import time
import json

with open('random_dense_datasets/random_datasets_015.json') as f:
    graphs=json.load(f)

for i in range(len(graphs)):
    g_labels={}
    for k,v in graphs[i][1].items():
        g_labels[int(k)]=v
    graphs[i][1]=g_labels

# Define dataframe
datos=pd.DataFrame(columns=['algorithm','S_n_nodes','S_n_edges','G_n_nodes','G_n_edges','time', 'memory_usage_peak', 'recursive_calls','found_mapping'])

# Save times to plot
times_vf2pp_nx = []
times_vf2pp = []
times_backtracking = []

# Start iteration using two 
i = 0
for S,G in itertools.permutations(graphs,2):
    print(i)
    # Check validity of graphs - if S has more vertices than G continue
    if len(list(S[1].keys())) > len(list(S[1].keys())):
        continue

    # Compute only 500 results
    if i == 500: break

    #-------------------------------
    #networkx data - this uses vf2
    try:
        tracemalloc.start()
        start = time.time()

        # Crear grafos
        S_nx = nx.Graph()
        S_nx.add_edges_from(S[0])
        for node, label in S[1].items():
            S_nx.nodes[node]['label'] = label

        G_nx = nx.Graph()
        G_nx.add_edges_from(G[0])
        for node, label in G[1].items():
            G_nx.nodes[node]['label'] = label

        # Comparador de nodos por label
        # node_match = isomorphism.categorical_node_match('label', None)
        # node_match = isomorphism.categorical_node_match()

        # Búsqueda de subgrafo isomorfo
        GM = nx.algorithms.isomorphism.GraphMatcher(G_nx, S_nx)
        ans = GM.subgraph_is_isomorphic()
        ans1 = ans


        end = time.time()
        current, peak = tracemalloc.get_traced_memory()

        # Guardar resultados
        resultados = pd.DataFrame([['nx_vf2', len(S[1]), len(S[0]), len(G[1]), len(G[0]), end - start, peak, 'NA', ans]], columns=datos.columns)
        times_vf2pp_nx.append(end - start)
        datos = pd.concat((datos, resultados), ignore_index=True)
        tracemalloc.stop()
    except:
        pass

    #---------------------------------------------
    # sacar datos de my_vf2pp
    tracemalloc.start()
    start=time.time()
    G_own=my_vf2pp.graph(list(G[1].keys()),G[0],G[1])
    S_own=my_vf2pp.graph(list(S[1].keys()),S[0],S[1])

    ans=(len(my_vf2pp.vf2pp(S_own,G_own))==len(S_own.nodes))

    end=time.time()
    recursive_calls = my_vf2pp.exec_record['recu_calls']
    current, peak = tracemalloc.get_traced_memory()
    resultados=pd.DataFrame([['our_vf2++',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,peak, recursive_calls, ans]],columns=datos.columns)

    datos=pd.concat((datos,resultados),ignore_index=True)
    times_vf2pp.append(end-start)

    #-----------------------
    #sacar datos de backtracking y fingerprints
    tracemalloc.start()
    start = time.time()
    G_own=my_vf2pp.graph(list(G[1].keys()),G[0],G[1])
    S_own=my_vf2pp.graph(list(S[1].keys()),S[0],S[1])
    solver = backtracking_y_fingerprint.BacktrackingFingerprintSolver(S_own, G_own)
    ans = solver.compute_isomorphism_backtracking()
    end = time.time()
    recursive_calls = solver.recurssion_count
    current, peak = tracemalloc.get_traced_memory()
    resultados=pd.DataFrame([['fingerprints and backtracking',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start, peak, recursive_calls, ans != {}]],columns=datos.columns)
    datos=pd.concat((datos,resultados),ignore_index=True)
    times_backtracking.append(end-start)
    tracemalloc.stop()

    if ans != {} and ans1 == False:
        print(S)
        print(G)
        

    i+=1

#####################
# Save dataset
datos.to_excel('results/all_results_random.xlsx')

###################### statistics by algorithm
grouped = datos.groupby('algorithm')

# Compute statistics
stats = grouped.agg(
    time_mean=('time', 'mean'),
    time_median=('time', 'median'),
    time_std=('time', 'std'),
    time_min=('time', 'min'),
    time_max=('time', 'max'),
    memory_mean=('memory_usage_peak', 'mean'),
    memory_std=('memory_usage_peak', 'std'),
    memory_min=('memory_usage_peak', 'min'),
    memory_max=('memory_usage_peak', 'max'),
    mapping_found_rate=('found_mapping', lambda x: x.mean() * 100)
).reset_index()

recursive_algorithms = ['fingerprints and backtracking', 'our_vf2++']
recursive_stats = (
    datos[datos['algorithm'].isin(recursive_algorithms)]
    .groupby('algorithm')
    .agg(
        recursive_calls_mean=('recursive_calls', 'mean'),
        recursive_calls_std=('recursive_calls', 'std'),
        recursive_calls_min=('recursive_calls', 'min'),
        recursive_calls_max=('recursive_calls', 'max')
    )
    .reset_index()
)

final_stats = pd.merge(stats, recursive_stats, on='algorithm', how='left')

# Save statistics in excel
final_stats.to_excel('results/results_89_DENSE_comparisson_stats.xlsx')

print(final_stats.to_markdown())
#########################################


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
