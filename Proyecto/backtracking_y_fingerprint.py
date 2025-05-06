from my_vf2pp import graph
import random
from itertools import combinations
import numpy as np

class BacktrackingFingerprintSolver:
    def __init__(self, S: graph, G: graph) -> None:
        """
        Initialize BacktrackingFingerprintSolver with two graphs S and G.
        """
        self.S = S
        self.G = G
        self.recurssion_count = 0 

        # Compute fingerprints for both graphs - obtain self.fingerprint_S and self.fingerprint_G
        self.build_fingerprint_map()

        # Compute candidates for each node in S based fingerprint compatibility
        self.candidates_x_node_S = {node:self.get_node_candidates(node) for node in self.S.nodes}

        # Sort nodes in S based on rarity
        self.orden_nodos_x_rareza = self.sort_candidates()

        # If any node doesnt have candidates, the isomorphism is impossible
        self.feasible_solution = all(len(candidates) > 0 for candidates in self.candidates_x_node_S.values())


    def build_fingerprint_map(self) -> None:
        """
        Builds a fingerprint map for both graphs S and G.
        The fingerprint is a tuple of (degree, sum of degrees of neighbors, number of triangles).
        Save the fingerprints in self.fingerprint_S and self.fingerprint_G.
        """

        def get_num_adjacent_triangles(G: graph, node: int) -> int:
            """
            Helper function to calculate the number of triangles associated with a node.
            Interate over all combinations of pairs of neighbors and count the triangles associated with the initial node.
                inputs: G: graph, node: int
                outputs: int - number of triangles associated with the node 
            """
            triangles = 0
            for neigh1, neigh2 in combinations(G.neighs[node], 2):
                if neigh2 in G.neighs[neigh1]:
                    triangles += 1
            return triangles
        
        # Define the functions to calculate the fingerprint components
        compute_degree = lambda G, node: G.deg(node)
        compute_sum_degrees_neighs = lambda G, node: sum(G.deg(neigh) for neigh in G.neighs[node])
        calcular_suma_de_cuadrados_grados_vecinos = lambda G, node: sum(G.deg(neigh)**2 for neigh in G.neighs[node])

        # Final fingerprint
        fingerprints_S = {node:(compute_degree(self.S, node), compute_sum_degrees_neighs(self.S, node), get_num_adjacent_triangles(self.S, node), calcular_suma_de_cuadrados_grados_vecinos(self.S, node)) for node in self.S.nodes}
        fingerprints_G = {node:(compute_degree(self.G, node), compute_sum_degrees_neighs(self.G, node), get_num_adjacent_triangles(self.G, node), calcular_suma_de_cuadrados_grados_vecinos(self.G, node)) for node in self.G.nodes}

        # Other fingerprint options:
        # fingerprints_S = {node:(calcular_grados(self.S, node), calcular_grados_vecinos(self.S, node), get_num_adjacent_triangles(self.S, node)) for node in self.S.nodes}
        # fingerprints_G = {node:(calcular_grados(self.G, node), calcular_grados_vecinos(self.G, node), get_num_adjacent_triangles(self.G, node)) for node in self.G.nodes}

        # fingerprints_S = {node:(compute_degree(self.S, node),) for node in self.S.nodes}
        # fingerprints_G = {node:(compute_degree(self.G, node),) for node in self.G.nodes}

        # Save final fingerprints
        self.fingerprint_S = fingerprints_S
        self.fingerprint_G = fingerprints_G

    def get_node_candidates(self, node_S: int) -> set:
        """
        Compute all the candidates for a node in S based on fingerprint compatibility. A node in G is a candidate if its fingerprint is greater than or equal to the fingerprint of the node in S and they have the same label
            inputs: node_S: int - node in S
            outputs: set - candidates in G that are compatible with node_S
        """
        
        def all_greater(p1:int, p2:int) -> bool:
            """
            Helper function to check if all components of a coordinate point p1 are less or equal to the corresponding components of p2.
                inputs: p1: int, p2: int - coordinates of the points
                outputs: bool - True if all components of p1 are less or equal to the corresponding components of p2, False otherwise
            """
            return all(c2 >= c1 for c1, c2 in zip(p1, p2))
        
        s_label = self.S.labels[node_S]
        candidatos = set()
        for node_G, fingerprint_G in self.fingerprint_G.items():
            g_label = self.G.labels[node_G]
            if all_greater(self.fingerprint_S[node_S],fingerprint_G) and s_label == g_label: 
                candidatos.add(node_G)
        return candidatos
    
    def sort_candidates(self) -> list:
        """
        Sort the nodes in S based on the number of candidates they have in G. The nodes with fewer candidates are processed first.
        This is done to reduce the search space and improve the efficiency of the backtracking algorithm.
            inputs: None
            outputs: list - sorted list of nodes in S based on the number of candidates they have in G
        """
        return [x[0] for x in sorted(self.candidates_x_node_S.items(), key=lambda x: len(x[1]))]
    
    def compute_isomorphism_backtracking(self, mapping = None, depth_level = 0) -> dict:
        """
        Compute the isomorphism between S and G using backtracking.
        The function recursively tries to map nodes from S to G and checks if the mapping is valid.
            inputs: mapping: dict - current mapping of nodes from S to G. If None, it initializes an empty mapping.
                    nivel_profundidad: int - current depth level in the backtracking search. Default is 0.
            outputs: dict - mapping of nodes from S to G if an isomorphism is found, otherwise an empty dictionary.
        """
        #count the number of recurssions
        self.recurssion_count += 1

        if mapping is None:
            mapping = {}

        #base case: all nodes have been mapped - verify isomorphism and return mapping
        if depth_level == len(self.S.nodes):
            return mapping.copy() if self.verify_solution(mapping) else {}
        
        #base case: there exists a node in S with no candidates in G
        if not self.feasible_solution:
            return {}
        
        #obtain current node in S to map according to the depth level
        node_S = self.orden_nodos_x_rareza[depth_level]

        #Process candidates for the current node
        for node_G_candidato in self.candidates_x_node_S[node_S]:
            # Verify if the node is compatible under the current mapping
            if self.is_compatible(node_S, node_G_candidato, mapping):
                # If compatible, add the mapping and continue the search
                mapping[node_S] = node_G_candidato
                res = self.compute_isomorphism_backtracking(mapping, depth_level + 1)
                # If a solution is found, return the mapping
                if res:
                    return res
                # If no solution is found, remove the node in the mapping and continue search
                del mapping[node_S]

        #return empty mapping if no isomorphism was found
        return {}
    
    def is_compatible(self, node_S:int, node_G_candidate:int, mapping:dict) -> bool:
        """
        Verify the candidate 
        1. Has not been mapped before
        2. Holds adjacencies with the current mapping
            inputs: node_S: int
                    node_G_candidate: int
                    mapping: dict
            outputs: bool - True if the conditions are met, False otherwise
        """

        if node_G_candidate in mapping.values():
            return False
        
        for neigh_S in self.S.neighs[node_S]:
            if neigh_S in mapping:
                mapped_neigh_G = mapping[neigh_S]
                if not mapped_neigh_G in self.G.neighs[node_G_candidate]:
                    return False
        return True
    
    def verify_solution(self, mapping:dict) -> bool:
        """
        Verify every node in S is mapped to a node in G and every edge in S is correctly mapped.
            inputs: mapping:dict
            outputs: bool - True if the conditions are met, False otherwise
        """

        if len(mapping) != len(self.S.nodes):
            return False
        
        for edge in self.S.edges:
            node1, node2 = edge
            mapped1, mapped2 = mapping[node1], mapping[node2]
            if not mapped2 in self.G.neighs[mapped1]:
                return False
        return True
    
    def graficar_mapeo(self, mapping:dict) -> None:
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.Graph()
        G.add_edges_from(self.G.edges)

        # Combine node number and mapping for better visualization
        node_labels = {node: f"{node}\n({next((k for k, v in mapping.items() if v == node), '-')})" for node in self.G.nodes}

        # Set node colors: light green if mapped, lightblue otherwise
        node_colors = ['lightblue' if node in mapping.values() else 'lightblue' for node in self.G.nodes]

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=node_colors, node_size=500, font_size=8, font_color='black')

        plt.show()


def graficar_grafo(G):
    import matplotlib.pyplot as plt
    import networkx as nx

    G_nx = nx.Graph()
    G_nx.add_edges_from(G.edges)

    # Combine node number and label for better visualization
    node_labels = {node: f"{node}\n{G.labels[node]}" for node in G.nodes}

    pos = nx.spring_layout(G_nx)
    nx.draw(G_nx, pos, with_labels=True, labels=node_labels, node_color='lightblue', node_size=500, font_size=8, font_color='black')

    plt.show()

    
if __name__ == "__main__":

    G_params = [[(119, 118), (118, 119), (120, 119), (119, 120), (121, 119), (119, 121), (122, 121), (121, 122), (123, 122), (122, 123), (124, 123), (123, 124), (125, 124), (124, 125), (126, 125), (125, 126), (127, 126), (126, 127), (127, 122), (122, 127), (128, 126), (126, 128), (129, 128), (128, 129), (130, 129), (129, 130), (130, 125), (125, 130), (131, 130), (130, 131), (132, 131), (131, 132), (133, 132), (132, 133), (134, 133), (133, 134), (134, 129), (129, 134), (135, 133), (133, 135), (136, 135), (135, 136), (137, 135), (135, 137)], {118: 0, 119: 0, 120: 2, 121: 2, 122: 0, 123: 0, 124: 0, 125: 0, 126: 0, 127: 0, 128: 0, 129: 0, 130: 0, 131: 0, 132: 0, 133: 0, 134: 0, 135: 1, 136: 2, 137: 2}]
    S_params = [[(152, 151), (151, 152), (153, 152), (152, 153), (154, 153), (153, 154), (155, 154), (154, 155), (156, 155), (155, 156), (156, 151), (151, 156), (157, 155), (155, 157), (158, 157), (157, 158), (159, 158), (158, 159), (159, 154), (154, 159), (160, 159), (159, 160), (161, 160), (160, 161), (162, 161), (161, 162), (163, 162), (162, 163), (163, 158), (158, 163), (164, 162), (162, 164), (165, 164), (164, 165), (166, 164), (164, 166)], { 151: 0, 152: 0, 153: 0, 154: 0, 155: 0, 156: 0, 157: 0, 158: 0, 159: 0, 160: 0, 161: 0, 162: 0, 163: 0, 164: 1, 165: 2, 166: 2}]

    G = graph(nodes=G_params[1].keys(),
              edges=G_params[0],
              labels=G_params[1])
    S = graph(nodes=S_params[1].keys(),
              edges=S_params[0],
              labels=S_params[1])
    
    # graficar_grafo(S)
    # graficar_grafo(G)

    solver = BacktrackingFingerprintSolver(S, G)
    print('Labels de S:', S.labels)
    print('Labels de G:', G.labels)
    print(solver.fingerprint_G)
    print(solver.fingerprint_S)
    mapeo = solver.compute_isomorphism_backtracking()
    
    if mapeo:
        print(f"Isomorfismo encontrado. Mapeo: {mapeo}")
        # solver.graficar_mapeo(mapeo)
    else:
        print("No se encontró isomorfismo.")

    print('El número de llamadas a recursion fue:',solver.recurssion_count)