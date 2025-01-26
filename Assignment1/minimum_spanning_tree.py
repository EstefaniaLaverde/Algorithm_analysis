

class Graph():
    def __init__(self, nodes: list[int], edges: list[tuple[int, int, int]]) -> None:
        self.nodes = nodes
        self.edges = edges

    ## FUNCION DE GRAFICACION HECHA CON GPT
    def draw_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

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

    def draw_digraph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

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


    def find(self, parent, x: int) -> int:
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal(self):

        mst= []

        parent = []
        rank = []

        self.edges = sorted(self.edges,
                            key=lambda item: item[2])

        for node in self.nodes:
            parent.append(node)
            rank.append(0)

        for u, v, w in self.edges:
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                mst.append((u,v,w))
                self.union(parent,rank,x,y)
        
        return mst
    

