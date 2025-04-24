# Implementando idea de fingerprint
import my_vf2pp as vf2pp
import plot_graph as pg
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


class Graph(vf2pp.graph):
    def __init__(self, nodes, edges, labels):
        super().__init__(nodes, edges, labels)
        self.edges = edges

    def numero_triangulos(self, node):
        triangulos = 0
        # Iterar sobre todas las combinaciones de pares de vecinos
        for neigh1, neigh2 in combinations(self.neighs[node], 2):
            if neigh2 in self.neighs[neigh1]:
                triangulos += 1
        return triangulos

    def update_fingerprints(self, max_values = None):
        if max_values is None:
            for node in self.nodes:
                self.labels[node] = (
                    len(self.neighs[node]),  # Grado del vertice
                    sum(len(self.neighs[neigh]) for neigh in self.neighs[node]),  # Suma de grados de los vecinos
                    self.numero_triangulos(node), # Numero de triangulos
                )
        else:
            max_grad, max_sum_grad, max_num_triang = max_values
            for node in self.nodes:
                grad = len(self.neighs[node])
                sum_grad = sum(len(self.neighs[neigh]) for neigh in self.neighs[node])
                num_triangulos = self.numero_triangulos(node)
                self.labels[node] = (
                    grad if grad <= max_grad else max_grad,  # Grado del vertice
                    sum_grad if sum_grad <= max_sum_grad else max_sum_grad,  # Suma de grados de los vecinos
                    num_triangulos if num_triangulos <= max_num_triang else max_num_triang, # Numero de triangulos
                )

def associate_fingerprints(S, G):
    S.update_fingerprints()
    max_values = max(S.labels.values())
    G.update_fingerprints(max_values)

if __name__ == '__main__':
    G1 = Graph(list(range(5)),
            [(0,1),(1,2),(2,3),(3,4),(4,0),(4,1)],
            {i:0 for i in range(5)})

    S = Graph(list(range(3)),
            [(0,1),(1,2),(2,0)],
            {i:0 for i in range(3)})
    
    associate_fingerprints(S, G1)

    print(G1.labels)
    print(S.labels)
    print(vf2pp.vf2pp(S,G1))

    # print(G1.labels)
    
    # G=nx.Graph()
    # G.add_nodes_from(G1.nodes)
    # G.add_edges_from(G1.edges)
    # nx.draw(G, with_labels=True)
    # plt.show()