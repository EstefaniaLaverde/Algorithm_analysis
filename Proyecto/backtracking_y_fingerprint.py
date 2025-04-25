from my_vf2pp import graph
import random
from itertools import combinations
import numpy as np

class GeneticIsomorphismSolver:
    def __init__(self, S: graph, G: graph, population_size=50, max_generations=1000):
        self.S = S
        self.G = G
        self.population_size = population_size
        self.max_generations = max_generations

        self.build_fingerprint_map()
        self.candidatos_x_nodoS = {node:self.calcular_candidatos(node) for node in self.S.nodes}
        self.orden_nodos_x_rareza = self.calcular_candidatos_ordenados()


    def build_fingerprint_map(self):
        def calcular_numero_triangulos(G, node):
            # Iterar sobre todas las combinaciones de pares de vecinos y contar los triangulos asociados al nodo inicial
            triangulos = 0
            for neigh1, neigh2 in combinations(G.neighs[node], 2):
                if neigh2 in G.neighs[neigh1]:
                    triangulos += 1
            return triangulos
        
        calcular_grados = lambda G, node: G.deg(node)
        calcular_grados_vecinos = lambda G, node: sum(G.deg(neigh) for neigh in G.neighs[node])
        calcular_suma_de_cuadrados_grados_vecinos = lambda G, node: sum(G.deg(neigh)**2 for neigh in G.neighs[node])

        fingerprints_S = {node:(calcular_grados(self.S, node), calcular_grados_vecinos(self.S, node), calcular_numero_triangulos(self.S, node), calcular_suma_de_cuadrados_grados_vecinos(self.S, node)) for node in self.S.nodes}

        fingerprints_G = {node:(calcular_grados(self.G, node), calcular_grados_vecinos(self.G, node), calcular_numero_triangulos(self.G, node), calcular_suma_de_cuadrados_grados_vecinos(self.G, node)) for node in self.G.nodes}
        # fingerprints_S = {node:(calcular_grados(self.S, node),) for node in self.S.nodes}
        # fingerprints_G = {node:(calcular_grados(self.G, node),) for node in self.G.nodes}

        # print("Fingerprints S:", fingerprints_S)
        # print("Fingerprints G:", fingerprints_G)
        self.fingerprint_S = fingerprints_S
        self.fingerprint_G = fingerprints_G

    def calcular_candidatos(self, node_S):
        # Calculo los candidatos para un nodo en S
        def todos_mayores(punto1, punto2):
            return all(c2 >= c1 for c1, c2 in zip(punto1, punto2))
        
        candidatos = set()
        for node_G, fingerprint_G in self.fingerprint_G.items():
            if todos_mayores(self.fingerprint_S[node_S],fingerprint_G):
                candidatos.add(node_G)
        # if not candidatos:
        #     print("No hay candidatos para el nodo", node_S)
        return candidatos
    
    def calcular_candidatos_ordenados(self):
        return [x[0] for x in sorted(self.candidatos_x_nodoS.items(), key=lambda x: len(x[1]))]
    
    def calcular_isomorfismo_backtracking(self, mapeo = {}, nivel_profundidad = 0):
        # Casos base: todos los nodos han sido mapeados
        if nivel_profundidad == len(self.S.nodes):
            return mapeo.copy() if self.verificar_solucion_isomorfismo(mapeo) else {}
        
        # Obtener el nodo actual de S a mapear
        nodo_S = self.orden_nodos_x_rareza[nivel_profundidad]

        # Si no hay candidatos para el nodo actual, no se encontrará isomorfismo
        if not self.candidatos_x_nodoS[nodo_S]:
            return {}

        # Proceso candidatos para nodo_S
        for node_G_candidato in self.candidatos_x_nodoS[nodo_S]:
            # Verificar si el nodo es compatible con el mapeo actual
            if self.es_compatible(nodo_S, node_G_candidato, mapeo):
                mapeo[nodo_S] = node_G_candidato
                res = self.calcular_isomorfismo_backtracking(mapeo, nivel_profundidad + 1)
                if res:
                    return res
                del mapeo[nodo_S] # Retroceso en la busqueda
        
    def es_compatible(self, nodo_S, node_G_candidato, mapeo):
        # Verifico que el candidato cumpla con:
        # 1. No ha sido mapeado antes
        # 2. Mantiene las adyacencias con los nodos ya mapeados

        if node_G_candidato in mapeo.values():
            return False
        
        for neigh_S in self.S.neighs[nodo_S]:
            if neigh_S in mapeo:
                mapped_neigh_G = mapeo[neigh_S]
                if not mapped_neigh_G in self.G.neighs[node_G_candidato]:
                    return False
        return True
    
    def verificar_solucion_isomorfismo(self, mapeo):
        # Verifico que todos los nodos de S tengan mapeo en G y que todas las adyacencias se mantengan
        if len(mapeo) != len(self.S.nodes):
            return False
        
        for node_S, node_G in mapeo.items():
            neighbours_S  = self.S.neighs[node_S]
            neighbours_G = self.G.neighs[node_G]

            # para cada vecino en S, el mapeo debe ser vecino en G
            for neigh_S in neighbours_S:
                if neigh_S in mapeo:
                    mapped_neigh_G = mapeo[neigh_S]
                    if not mapped_neigh_G in neighbours_G:
                        return False
                    
        return True
    
    def graficar_mapeo(self, mapeo):
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.Graph()
        G.add_edges_from(self.G.edges)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black')
        
        # Graficar el mapeo
        for node_S, node_G in mapeo.items():
            plt.annotate(f"{node_S} -> {node_G}", xy=pos[node_G], xytext=(5, 5), textcoords="offset points", fontsize=8, color='red')

        plt.show()


def graficar_grafo(G):
    import matplotlib.pyplot as plt
    import networkx as nx

    G_nx = nx.Graph()
    G_nx.add_edges_from(G.edges)

    pos = nx.spring_layout(G_nx)
    nx.draw(G_nx, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black')
    
    plt.show()

    
if __name__ == "__main__":

    S = graph(list(range(3)),
            [(0,1),(1,2),(0,2)],
            {i:0 for i in range(3)})

    G = graph(list(range(5)),
            [(0,1),(1,2),(2,3),(3,4)],
            {i:0 for i in range(4)})

    # graficar_grafo(S)
    # graficar_grafo(G)

    solver = GeneticIsomorphismSolver(S, G, population_size=10)
    mapeo = solver.calcular_isomorfismo_backtracking()
    
    if mapeo:
        print(f"¡Isomorfismo encontrado! Mapeo: {mapeo}")
        # solver.graficar_mapeo(mapeo)
    else:
        print("No se encontró isomorfismo.")