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
        """
        Finds the root of the set that includes x.

        This method is part of the disjoint-set data structure. It finds the root of the set that includes x by recursively following the parent pointers until it finds the root (i.e., a node that is its own parent).

        Parameters:
        parent (list[int]): The parent array of the disjoint-set data structure.
        x (int): The node to find the root for.

        Returns:
        int: The root of the set that includes x.
        """
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent: list[int], rank: list[int], x: int, y: int) -> None:
        """
        Merges the sets that include x and y.

        This method is part of the disjoint-set data structure. It merges the sets that include x and y by making the root of one set the parent of the root of the other set. The rank is used to optimize the tree structure by making the tree with the smaller rank a subtree of the other tree.

        Parameters:
        parent (list[int]): The parent array of the disjoint-set data structure.
        rank (list[int]): The rank array of the disjoint-set data structure.
        x (int): The first node.
        y (int): The second node.
        """
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal(self) -> list[tuple[int, int, int]]:
        """
        Implements Kruskal's algorithm to find the minimum spanning tree (MST) of the graph.

        This method sorts the edges by their weight and then iterates over them. For each edge, it checks if the edge connects two different components (i.e., if the roots of the two nodes are different). If it does, it adds the edge to the MST and merges the two components.

        Returns:
        list[tuple[int, int, int]]: The edges of the minimum spanning tree.
        """
        mst = []

        parent = [i for i in range(len(self.nodes))]
        rank = [0] * len(self.nodes)

        # Sort the edges by their weight
        self.edges = sorted(self.edges, key=lambda item: item[2])

        for u, v, w in self.edges:
            x = self.find(parent, self.node_to_index[u])
            y = self.find(parent, self.node_to_index[v])

            if x != y:
                mst.append((u, v, w))
                self.union(parent, rank, x, y)

        return mst
    



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python .\\Assignment1\\ejercicio5_final.py <input_file.in> <output_file.out>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    results = []

    with open(input_file) as f:
        content = f.read()  # Read the entire file content
        sections = [section.strip() for section in content.split('\n\n') if section.strip()]  # Split by double newlines

    for section in sections:
        lines = section.splitlines()
        nodes = list(map(int, lines[0].split()))
        m = int(lines[1])

        edges = []
        for i in range(2, 2 + m):
            a, b, c = map(int, lines[i].split())
            edges.append((a, b, c))

        graph = Graph(nodes, edges)

        # Run Kruskal's algorithm
        mst = graph.kruskal()

        # Save the length of the MST and the edges
        results.append((len(mst), mst))

        print(len(mst))
        for a, b, c in mst:
            print(a,b,c)


    # Save results
    with open(output_file, 'w') as f:
        for length, mst in results:
            f.write(f"{length}\n")  # Write the length of the MST
            for a, b, c in mst:
                f.write(f"{a} {b} {c}\n")  # Write the edges of the MST
            f.write("\n")
