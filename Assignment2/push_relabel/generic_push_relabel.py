import time
import sys
from collections import deque

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


class Graph:
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



    G=Graph(n)

    for u,v,c in edges:
        G.add_edge(u,v,c)

    #medir tiempo ejecucion de generic_push_relabel
    start=time.time()
    edges_flow,total_flow=G.generic_push_relabel(source = 0, sink = n-1)
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



