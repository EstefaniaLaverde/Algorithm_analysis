import sys
import networkx as nx
import matplotlib.pyplot as plt



class Graph():
    def __init__(self, nodes: list[int], edges: list[tuple[int, int, int]]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.node_to_index = {node: i for i, node in enumerate(nodes)}


    ## FUNCION DE GRAFICACION HECHA CON GPT
    def draw_graph(self) -> None:
        G = nx.Graph()
        G.add_nodes_from(self.nodes)

        for u, v, w in self.edges:
            G.add_edge(u, v, weight=w)

        edge_labels = {(u, v): w for u, v, w in self.edges}

        pos = nx.spring_layout(G)  
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Graph Visualization")
        plt.show()

    def draw_digraph(self) -> None:

        G = nx.DiGraph()
        G.add_nodes_from(self.nodes)

        for u, v, w in self.edges:
            G.add_edge(u, v, weight=w)

        edge_labels = {(u, v): w for u, v, w in self.edges}

        pos = nx.spring_layout(G) 
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Directed Graph Visualization")
        plt.show()


    def find(self, parent: list[int], x: int) -> int:
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent: list[int], rank: list[int], x: int, y: int) -> None:
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal(self) -> list[tuple[int, int, int]]:

        mst= []

        parent = [i for i in range(len(self.nodes))]
        rank = [0] * len(self.nodes)

        self.edges = sorted(self.edges,
                            key=lambda item: item[2])


        for u, v, w in self.edges:
            x = self.find(parent, self.node_to_index[u]) 
            y = self.find(parent, self.node_to_index[v])

            if x != y:
                mst.append((u,v,w))
                self.union(parent,rank,x,y)
        
        return mst
    



if __name__=='__main__':
    #leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b,c=map(int,f.readline().split())
            edges.append((a,b,c))

    graph = Graph(nodes, edges)

    # Run Kruskal's algorithm
    mst = graph.kruskal()

    print(len(mst))
    for a,b,c in mst:
        print(a,b,c)
