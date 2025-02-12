
from collections import deque
import sys
import time


class Graph:
    def __init__(self,n: int, edges: list[tuple[int,int,int]]) -> None:
        """
        Inicializa un grafo con n nodos y una lista de edges.

        Inputs:
        - n (int): El número de nodos en el grafo.
        - edges (list[tuple[int,int,int]]): Una lista de edges, cada edge representado como una tupla de tres elementos: el nodo de origen, el nodo de destino, y la capacidad del edge.
        """
        self.edges_out=[{} for i in range(n)]

        # Conjunto para guardar las parejas de nodos que ya tienen un eje entre ellos
        found_edges=set()
        for u,v,c in edges:
            self.edges_out[u][v]=c

            # Lanzar un error si se ingresa un grafo con múltiples edges entre el mismo par de nodos
            # Obtener el mínimo y el máximo para tener una representación canónica del eje (u,v) sin importar la dirección
            (a,b)=(min(u,v),max(u,v))
            if (a,b) in found_edges:
                raise AssertionError("el grafo tiene múltiples edges para un mismo par de nodos")
            found_edges.add((a,b))


    def get_path(self, src_node: int, target_node: int) -> list[int]:
        """
        Retorna una lista de nodos que representa el camino entre src_node y target_node en el grafo.
        Retorna lista vacía en caso de que no haya camino.

        Inputs:
        - src_node (int): El nodo fuente del camino.
        - target_node (int): El nodo destino del camino.

        Outputs:
        - list[int]: Una lista de nodos que representa el camino entre src_node y target_node. Retorna lista vacía si no hay camino.
        """
        n = len(self.edges_out)

        # Inicializa una lista para guardar el padre de cada nodo en el BFS, para reconstruir el camino.
        # -1 indica que el nodo no ha sido visitado.
        father = [-1 for i in range(n)]
        queue = deque()

        # Marca el nodo fuente como su propio padre y lo agrega a la cola.
        father[src_node] = src_node
        queue.append(src_node)

        while queue:
            node = queue.popleft()

            # Reconstruye el camino si se encuentra el nodo destino.
            if node == target_node:
                path = []
                while father[node] != node:
                    path.append(node)
                    node = father[node]
                path.append(node)

                path.reverse()
                return path

            for neigh in self.edges_out[node]:
                # Solo transita edges con peso mayor a 0 y hacia nodos no visitados.
                if self.edges_out[node][neigh] > 0 and father[neigh] == -1:
                    queue.append(neigh)
                    father[neigh] = node
        
        return []


    def edmond_karps(self) -> tuple[list[tuple[int, int, int]], int]:
        """
        Implementa el algoritmo de Edmonds-Karp para encontrar el flujo máximo en un grafo de flujo.
        Retorna una lista de edges con sus respectivos flujos y el flujo total del grafo.

        Outputs:
        - list[tuple[int, int, int]]: Una lista de edges, cada edge representado como una tupla de tres elementos: el nodo de origen, el nodo de destino, y el flujo en ese edge.
        - int: El flujo total del grafo.
        """
        n = len(self.edges_out)

        # Inicializa la capacidad máxima de un edge en el grafo.
        max_cap = 0
        # Crea el grafo residual.
        residual = Graph(n, [])
        for u in range(n):
            for v in self.edges_out[u]:
                c = self.edges_out[u][v]
                residual.edges_out[u][v] = c
                residual.edges_out[v][u] = 0
                max_cap = max(max_cap, c)

        src_node = 0
        sink_node = n - 1

        while True:
            path = residual.get_path(src_node, sink_node)
            if path:
                # Determina cuánto flujo se puede agregar por ese camino.
                min_res_on_path = max_cap
                for i in range(len(path) - 1):
                    min_res_on_path = min(min_res_on_path, residual.edges_out[path[i]][path[i + 1]])

                # Agrega flujo por el camino.
                for i in range(len(path) - 1):
                    u = path[i]
                    v = path[i + 1]

                    # Obtener capacidad del edge en el grafo original.
                    if v in self.edges_out[u]:
                        edge_capacity = self.edges_out[u][v]
                    else:
                        edge_capacity = self.edges_out[v][u]

                    # Actualiza flujo en el residual.
                    residual.edges_out[u][v] -= min_res_on_path
                    residual.edges_out[v][u] = edge_capacity - residual.edges_out[u][v]
            else:
                break

        # Crea lista con flujos en el formato definido.
        edges_flow = []
        for u in range(n):
            for v in self.edges_out[u]:
                # El residuo es el espacio sobrante, así con la resta obtenemos el espacio ocupado.
                edges_flow.append((u, v, self.edges_out[u][v] - residual.edges_out[u][v]))

        # Calcula el flujo total, medimos el flujo que sale de la fuente.
        total_flow = 0
        for edge in edges_flow:
            if edge[0] == src_node:
                total_flow += edge[2]

        return edges_flow, total_flow



if __name__=='__main__':
    #input_path: path del archivo con el grafo que queremos evaluar
    #output_path: path donde guaramos los resultados del procesamiento

    input_path=sys.argv[1]
    output_path=sys.argv[2]

    #leer grafo desde archivo txt
    with open(input_path) as f:
        n=int(f.readline())
        edges=[]

        line=f.readline()
        while line:
            a,b,c=map(int,line.split())
            line=f.readline()
            edges.append((a,b,c))



    G=Graph(n,edges)

    #medir tiempo ejecucion de edmond_karps
    start=time.time()
    edges_flow,total_flow=G.edmond_karps()
    end=time.time()

    #guardar resultados
    with open(output_path,'w') as f:
        #descipcion de flujo en cada eje
        for edge in edges_flow:
            f.write(' '.join(map(str,edge))+'\n')
        #flujo total del grafo
        f.write(str(total_flow)+'\n')
        #tiempo de ejecucion
        f.write(str(end-start)+'\n')

