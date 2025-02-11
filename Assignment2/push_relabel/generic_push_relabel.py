import time


class Edge:
    def __init__(self, capacity, flow=0):
        self.capacity = capacity
        self.flow = flow


class Vertex:
    def __init__(self, excess=0, height=0):
        self.excess = excess
        self.height = height


class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.edges = {}
        self.vertices = [Vertex() for _ in range(num_vertices)]
        self.orig_edges =[]

    def add_edge(self, u, v, capacity):
        if (u,v) in self.edges:
            raise AssertionError("el grafo tiene multiples edges para un mismo par de nodos")
        self.edges[(u, v)] = Edge(capacity)
        self.edges[(v, u)] = Edge(0)
        self.orig_edges.append((u, v))
                

    def get_neighbors(self, u):
        return [v for (x, v) in self.edges if x == u]

    def preflow(self, source):

        # inicializacion de la altura del origen
        self.vertices[source].height = self.num_vertices
        for v in self.get_neighbors(source):
            edge = self.edges[(source, v)]

            # saturar los nodos conectados al origen, aumentar el excess en el nodo y reducirlo en el origen
            edge.flow = edge.capacity
            self.vertices[v].excess += edge.flow
            self.vertices[source].excess -= edge.flow

            # flujo en la red residual
            self.edges[(v, source)].flow = -edge.flow

    def push(self, u, v):
        edge = self.edges[(u, v)]
        residual = edge.capacity - edge.flow
        if self.vertices[u].excess > 0 and residual > 0 and self.vertices[u].height == self.vertices[v].height + 1:
            delta = min(self.vertices[u].excess, residual)
            edge.flow += delta
            self.edges[(v, u)].flow -= delta
            self.vertices[u].excess -= delta
            self.vertices[v].excess += delta
            return True
        return False

    def relabel(self, u):
        min_height = float('inf')

        for v in self.get_neighbors(u):
            edge = self.edges[(u, v)]
            if edge.capacity - edge.flow > 0:
                min_height = min(min_height, self.vertices[v].height)
        if min_height < float('inf'):
            self.vertices[u].height = min_height + 1

    def generic_push_relabel(self, source=0, sink=None):
        if sink is None:
            sink = self.num_vertices - 1

        self.preflow(source)

        active = [u for u in range(self.num_vertices) if u not in (source, sink) and self.vertices[u].excess > 0]

        while active:
            u = active.pop(0)
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
        
        edges_flow=[]
        for edge in self.orig_edges:
            edges_flow.append((edge[0], edge[1], self.edges[edge].flow))

        return edges_flow, self.vertices[sink].excess






if __name__=='__main__':
    #input_path: path del archivo con el grafo que queremos evaluar
    #output_path: path donde guaramos los resultados del procesamiento

    input_path="C:/Users/pablo/OneDrive/Documents/Universidad/Dalgo2/Algorithm_analysis/Assignment2/push_relabel/tests/test1.txt"
    output_path="C:/Users/pablo/OneDrive/Documents/Universidad/Dalgo2/Algorithm_analysis/Assignment2/push_relabel/results/result1.txt"

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

    #medir tiempo ejecucion de edmond_karps
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



