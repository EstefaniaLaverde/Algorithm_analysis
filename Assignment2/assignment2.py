from collections import deque
import sys
import time


class Graph_EdmondsKarp:
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
        residual = Graph_EdmondsKarp(n, [])
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
    

class Edge:
    def __init__(self, capacity:int, flow:int=0) -> None:
        """
        Inicializa un objeto Edge.

        Args:
            capacity (int): La capacidad máxima del borde.
            flow (int, opcional): El flujo inicial. Por defecto es 0.
        """
        self.capacity = capacity
        self.flow = flow


class Vertex:
    def __init__(self, excess:int=0, height:int=0) -> None:
        """
        Inicializa un objeto Vertex.

        Args:
            excess (int, opcional): El exceso de flujo en el vértice. Por defecto es 0.
            height (int, opcional): La altura del vértice. Por defecto es 0.
        """
        self.excess = excess
        self.height = height


class Graph_PushRelabel:
    def __init__(self, num_vertices:int) -> None:
        """
        Inicializa los atributos del grafo.

        Args:
            num_vertices (int): El número de vértices en el grafo.

        Atributos:
            num_vertices (int): El número de vértices en el grafo.
            edges (dict): Un diccionario que mapea pares de vértices a objetos Edge.
            vertices (list): Una lista de objetos Vertex, cada uno representando un vértice.
            orig_edges (list): Una lista de pares de vértices, representando los bordes originales del grafo.
        """
        self.num_vertices = num_vertices
        self.edges = {}
        self.vertices = [Vertex() for _ in range(num_vertices)]
        self.orig_edges =[]

    def add_edge(self, u:int, v:int, capacity:int) -> None:
        """
        Agrega un eje al grafo.

        Args:
            u (int): El índice del vértice de origen.
            v (int): El índice del vértice de destino.
            capacity (int): La capacidad del eje.

        Raises:
            AssertionError: Si el grafo ya tiene un eje entre los vértices u y v.
        """
        if (u,v) in self.edges:
            raise AssertionError("el grafo tiene multiples edges para un mismo par de nodos")
        self.edges[(u, v)] = Edge(capacity)
        self.edges[(v, u)] = Edge(0)
        self.orig_edges.append((u, v))
                

    def get_neighbors(self, u:int):
        """
        Retorna una lista de los vecinos del vértice u.

        Args:
            u (int): El índice del vértice del cual se desean obtener los vecinos.

        Returns:
            list: Una lista de índices de los vecinos del vértice u.
        """
        return [v for (x, v) in self.edges if x == u]

    def preflow(self, source: int) -> None:
        """
        Inicializa el flujo en el grafo, saturando los bordes que salen del vértice fuente.

        Args:
            source (int): El índice del vértice fuente.

        Raises:
            AssertionError: Si el índice del vértice fuente es inválido.
        """
        if source < 0 or source >= self.num_vertices:
            raise AssertionError("Índice del vértice fuente inválido")

        # Inicializacion de la altura del origen
        self.vertices[source].height = self.num_vertices
        for v in self.get_neighbors(source):
            edge = self.edges[(source, v)]

            # Saturar los nodos conectados al origen, aumentar el excess en el nodo y reducirlo en el origen
            edge.flow = edge.capacity
            self.vertices[v].excess += edge.flow
            self.vertices[source].excess -= edge.flow

            # Flujo en la red residual
            self.edges[(v, source)].flow = -edge.flow

    def push(self, u: int, v: int) -> bool:
        """
        Intenta empujar flujo desde el vértice u hacia el vértice v.

        Args:
            u (int): El índice del vértice de origen.
            v (int): El índice del vértice de destino.

        Returns:
            bool: Retorna True si se pudo empujar flujo, False de lo contrario.
        """
        edge = self.edges[(u, v)]  # Obtener el eje entre u y v
        residual = edge.capacity - edge.flow  # Calcular la capacidad residual del eje
        
        if self.vertices[u].excess > 0 and residual > 0 and self.vertices[u].height == self.vertices[v].height + 1:
            delta = min(self.vertices[u].excess, residual)
            edge.flow += delta
            self.edges[(v, u)].flow -= delta
            self.vertices[u].excess -= delta
            self.vertices[v].excess += delta
            return True
        return False

    def relabel(self, u: int) -> None:
        """
        Reetiqueta el vértice u ajustando su altura según la altura de sus vecinos.

        Args:
            u (int): El índice del vértice a reetiquetar.
        """
        min_height = float('inf')

        for v in self.get_neighbors(u):
            edge = self.edges[(u, v)]
            if edge.capacity - edge.flow > 0:
                min_height = min(min_height, self.vertices[v].height)
        if min_height < float('inf'):
            self.vertices[u].height = min_height + 1

    def generic_push_relabel(self, source: int = 0, sink: int = None) -> tuple[list[tuple[int, int, int]], int]:
        """
        Implementa el algoritmo genérico de push-relabel para determinar el flujo máximo en una red.

        Args:
            source (int): El índice del nodo fuente. Por defecto es 0.
            sink (int): El índice del nodo destino. Si no se proporciona, se asume que es el último nodo. Por defecto es None.

        Returns:
            Tuple[List[Tuple[int, int, int]], int]: Una tupla que contiene una lista de tuplas que representan el flujo en cada eje y el flujo total.
        """
        if sink is None:
            sink = self.num_vertices - 1

        self.preflow(source)

        # Usamos deque para una cola eficiente en O(1) para popleft() y append()
        active = deque(u for u in range(self.num_vertices)
                    if u not in (source, sink) and self.vertices[u].excess > 0)

        while active:
            u = active.popleft()
            pushed = False
            for v in self.get_neighbors(u):
                if self.push(u, v):
                    pushed = True
                    if v not in (source, sink) and self.vertices[v].excess > 0 and v not in active:
                        active.append(v)

                    if self.vertices[u].excess == 0:
                        break
            if self.vertices[u].excess > 0:
                if not pushed:
                    self.relabel(u)
                active.append(u)
        
        edges_flow = []
        for edge in self.orig_edges:
            edges_flow.append((edge[0], edge[1], self.edges[edge].flow))

        return edges_flow, self.vertices[sink].excess
    
def main(input_path: str, output_path: str):
    """
    Ejecuta el algoritmo de Edmonds-Karp y Push-Relabel para determinar el flujo máximo en un grafo de flujo.
    Lee el grafo desde un archivo de texto, ejecuta ambos algoritmos, mide el tiempo de ejecución y
    guarda los resultados en un archivo de texto.

    Args:
        input_path (str): El path del archivo de texto que contiene el grafo a evaluar.
        output_path (str): El path donde se guardarán los resultados del procesamiento.

    Returns:
        None
    """
    # leer grafo desde archivo txt
    with open(input_path) as f:
        n = int(f.readline())
        edges = []

        line = f.readline()
        while line:
            a, b, c = map(int, line.split())
            line = f.readline()
            edges.append((a, b, c))

    # Ejecutar Edmonds Karp
    GraphEdmondsKarp = Graph_EdmondsKarp(n, edges)

    # medir tiempo ejecucion de edmond_karps
    start = time.time()
    edges_flow_ek, total_flow_ek = GraphEdmondsKarp.edmond_karps()
    end = time.time()
    time_ek = end - start

    # Ejecutar Push Relabel
    GraphPushRelabel = Graph_PushRelabel(n)

    for u, v, c in edges:
        GraphPushRelabel.add_edge(u, v, c)

    # medir tiempo ejecucion de push relabel
    start = time.time()
    edges_flow_pr, total_flow_pr = GraphPushRelabel.generic_push_relabel(source=0, sink=n-1)
    end = time.time()
    time_pr = end - start

    # guardar resultados
    with open(output_path, 'w') as f:
        f.write('Results Edmonds Karp' + '\n')
        # descipcion de flujo en cada eje
        for edge in edges_flow_ek:
            f.write(' '.join(map(str, edge)) + '\n')
        # flujo total del grafo
        f.write(str(total_flow_ek) + '\n')
        # tiempo de ejecucion
        f.write(str(time_ek) + '\n')

        f.write('Results Push Relabel' + '\n')
        # descipcion de flujo en cada eje
        for edge in edges_flow_pr:
            f.write(' '.join(map(str, edge)) + '\n')
        # flujo total del grafo
        f.write(str(total_flow_pr) + '\n')
        # tiempo de ejecucion
        f.write(str(time_pr) + '\n')


if __name__ == '__main__':
    # Ejecutar funcion main
    input_path=sys.argv[1]
    output_path=sys.argv[2]

    main(input_path, output_path)