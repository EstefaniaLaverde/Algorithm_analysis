# searching NO2 isomorphisms in the biological dataset
from backtracking_y_fingerprint import BacktrackingFingerprintSolver, graficar_grafo
from my_vf2pp import vf2pp
import biological_datasets.read_dataset as rd
from my_vf2pp import graph as grp
import time
from itertools import combinations
from tqdm import tqdm

G_graphs = rd.read_and_process_dataset('biological_datasets/mutag.txt')

Gs = []
for graph in G_graphs:
    G = grp(nodes=list(graph[1].keys()),
                    edges = graph[0],
                    labels = graph[1])  
    Gs.append(G)

# Generate combinations of graphs
graph_pairs = list(combinations(Gs, 2))
print('Numero de pares:', len(graph_pairs))
graph_pairs = graph_pairs[:100]

graphs_with_isomorphism = []
isomorphisms_backtracking = []
isomorphisms_vf2pp = []
times_backtracking = []
times_vf2pp = []

for i, (S, G) in tqdm(enumerate(graph_pairs), total=len(graph_pairs), desc="Processing graph pairs"):
    # graficar_grafo(S)
    # graficar_grafo(G)
    start_time = time.time()
    solver = BacktrackingFingerprintSolver(S, G)
    mapping = solver.compute_isomorphism_backtracking()
    isomorphisms_backtracking.append(mapping)
    end_time = time.time()
    times_backtracking.append(end_time - start_time)

    start_time = time.time()
    isomorphisms_vf2pp.append(vf2pp(S, G))
    end_time = time.time()
    times_vf2pp.append(end_time - start_time)

    if mapping != {}:
        graphs_with_isomorphism.append((S,G))
        

print("Isomorphisms found backtracking:", len([mapping for mapping in isomorphisms_backtracking if mapping != {}]))
print("Isomorphisms found vf2pp:", len([mapping for mapping in isomorphisms_vf2pp if mapping != {}]))

# ##################################
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Crear un rango para el eje x basado en el número de grafos
x = np.arange(len(times_backtracking))

# Crear un DataFrame para usar con seaborn
import pandas as pd
data = pd.DataFrame({
    "Graph Index": np.concatenate([x, x]),
    "Time (seconds)": times_backtracking + times_vf2pp,
    "Method": ["Backtracking"] * len(times_backtracking) + ["VF2++"] * len(times_vf2pp)
})

# Configurar el estilo de seaborn
sns.set(style="whitegrid")

# Crear la gráfica
plt.figure(figsize=(10, 6))
sns.lineplot(data=data, x="Graph Index", y="Time (seconds)", hue="Method", marker="o")

# Etiquetas y título
plt.xlabel("Graph Index")
plt.ylabel("Time (seconds)")
plt.title("Comparison of Execution Times")
plt.legend(title="Method")

# Mostrar la gráfica
plt.show()

