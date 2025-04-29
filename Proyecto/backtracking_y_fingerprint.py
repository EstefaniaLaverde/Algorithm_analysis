from my_vf2pp import graph
import random
from itertools import combinations
import numpy as np

class BacktrackingFingerprintIsomorphismSolver:
    def __init__(self, S: graph, G: graph):
        self.S = S
        self.G = G

        self.build_fingerprint_map()
        self.candidatos_x_nodoS = {node:self.calcular_candidatos(node) for node in self.S.nodes}
        self.orden_nodos_x_rareza = self.ordenar_candidatos()


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

        # fingerprints_S = {node:(calcular_grados(self.S, node), calcular_grados_vecinos(self.S, node), calcular_numero_triangulos(self.S, node)) for node in self.S.nodes}
        # fingerprints_G = {node:(calcular_grados(self.G, node), calcular_grados_vecinos(self.G, node), calcular_numero_triangulos(self.G, node)) for node in self.G.nodes}

        fingerprints_S = {node:(calcular_grados(self.S, node), calcular_grados_vecinos(self.S, node), calcular_numero_triangulos(self.S, node), calcular_suma_de_cuadrados_grados_vecinos(self.S, node)) for node in self.S.nodes}
        fingerprints_G = {node:(calcular_grados(self.G, node), calcular_grados_vecinos(self.G, node), calcular_numero_triangulos(self.G, node), calcular_suma_de_cuadrados_grados_vecinos(self.G, node)) for node in self.G.nodes}

        # fingerprints_S = {node:(calcular_grados(self.S, node),) for node in self.S.nodes}
        # fingerprints_G = {node:(calcular_grados(self.G, node),) for node in self.G.nodes}

        self.fingerprint_S = fingerprints_S
        self.fingerprint_G = fingerprints_G

    def calcular_candidatos(self, node_S):
        # Calculo los candidatos para un nodo en S
        def todos_mayores(punto1, punto2):
            return all(c2 >= c1 for c1, c2 in zip(punto1, punto2))
        
        s_label = self.S.labels[node_S]
        candidatos = set()
        for node_G, fingerprint_G in self.fingerprint_G.items():
            g_label = self.G.labels[node_G]
            if todos_mayores(self.fingerprint_S[node_S],fingerprint_G) and s_label == g_label:
                candidatos.add(node_G)
        # if not candidatos:
        #     print("No hay candidatos para el nodo", node_S)
        return candidatos
    
    def ordenar_candidatos(self):
        # se ordenan los nodos según que tan 'raros' son. Es decirm de menor a mayor número de candidatos
        return [x[0] for x in sorted(self.candidatos_x_nodoS.items(), key=lambda x: len(x[1]))]
    
    def calcular_isomorfismo_backtracking(self, mapeo = None, nivel_profundidad = 0):
        if mapeo is None:
            mapeo = {}

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
            # print(f"Probando mapeo: {nodo_S} -> {node_G_candidato} con mapeo actual: {mapeo}")
            # Verificar si el nodo es compatible con el mapeo actual
            if self.es_compatible(nodo_S, node_G_candidato, mapeo):
                mapeo[nodo_S] = node_G_candidato
                res = self.calcular_isomorfismo_backtracking(mapeo, nivel_profundidad + 1)
                if res:
                    return res
                del mapeo[nodo_S] # Retroceso en la busqueda

        return {} # Se retrocedió hasta el primer nodo y no se encontro isomorfismo
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

    # Obtener los labels de los nodos
    node_labels = {node: G.labels[node] for node in G.nodes}

    pos = nx.spring_layout(G_nx)
    nx.draw(G_nx, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black')

    # Dibujar los labels de los nodos
    nx.draw_networkx_labels(G_nx, pos, labels=node_labels, font_size=10, font_color='red')

    plt.show()

    
if __name__ == "__main__":

    # S = graph(list(range(3)),
    #         [(0,1),(1,2),(0,2)],
    #         {i:0 for i in range(3)})

    # G = graph(list(range(5)),
    #         [(0,1),(1,2),(2,3),(3,4)],
    #         {i:0 for i in range(5)})


    G_params = [[(119, 118), (118, 119), (120, 119), (119, 120), (121, 119), (119, 121), (122, 121), (121, 122), (123, 122), (122, 123), (124, 123), (123, 124), (125, 124), (124, 125), (126, 125), (125, 126), (127, 126), (126, 127), (127, 122), (122, 127), (128, 126), (126, 128), (129, 128), (128, 129), (130, 129), (129, 130), (130, 125), (125, 130), (131, 130), (130, 131), (132, 131), (131, 132), (133, 132), (132, 133), (134, 133), (133, 134), (134, 129), (129, 134), (135, 133), (133, 135), (136, 135), (135, 136), (137, 135), (135, 137)], {118: 0, 119: 0, 120: 2, 121: 2, 122: 0, 123: 0, 124: 0, 125: 0, 126: 0, 127: 0, 128: 0, 129: 0, 130: 0, 131: 0, 132: 0, 133: 0, 134: 0, 135: 1, 136: 2, 137: 2}]
    S_params = [[(152, 151), (151, 152), (153, 152), (152, 153), (154, 153), (153, 154), (155, 154), (154, 155), (156, 155), (155, 156), (156, 151), (151, 156), (157, 155), (155, 157), (158, 157), (157, 158), (159, 158), (158, 159), (159, 154), (154, 159), (160, 159), (159, 160), (161, 160), (160, 161), (162, 161), (161, 162), (163, 162), (162, 163), (163, 158), (158, 163), (164, 162), (162, 164), (165, 164), (164, 165), (166, 164), (164, 166)], { 151: 0, 152: 0, 153: 0, 154: 0, 155: 0, 156: 0, 157: 0, 158: 0, 159: 0, 160: 0, 161: 0, 162: 0, 163: 0, 164: 1, 165: 2, 166: 2}]

    G = graph(nodes=G_params[1].keys(),
              edges=G_params[0],
              labels=G_params[1])
    S = graph(nodes=S_params[1].keys(),
              edges=S_params[0],
              labels=S_params[1])
    
    graficar_grafo(S)
    graficar_grafo(G)

    solver = BacktrackingFingerprintIsomorphismSolver(S, G)
    print('Labels de S:', S.labels)
    print('Labels de G:', G.labels)
    print(solver.fingerprint_G)
    print(solver.fingerprint_S)
    mapeo = solver.calcular_isomorfismo_backtracking()
    
    if mapeo:
        print(f"Isomorfismo encontrado. Mapeo: {mapeo}")
        solver.graficar_mapeo(mapeo)
    else:
        print("No se encontró isomorfismo.")