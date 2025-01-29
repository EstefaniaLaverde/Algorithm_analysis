import sys

class Graph():
    def __init__(self, nodes: list[int], edges: list[tuple[int, int, int]]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.node_to_index = {node: i for i, node in enumerate(nodes)}

    def find(self, parent: list[int], x: int) -> int:
        """
        Encuentra el representante del conjunto al que pertenece x

        Parameters:
        parent (list[int]): El arreglo de padres de la estructura de datos disjoint-set.
        x (int): El nodo para el cual encontrar la raíz.

        Retorna:
        int: La raíz del conjunto que incluye a x.
        """
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent: list[int], rank: list[int], x: int, y: int) -> None:
        """
        Une dos conjuntos disjuntos

        Parameters:
        parent (list[int]): El arreglo de padres de la estructura de datos disjoint-set.
        rank (list[int]): El arreglo de rangos de la estructura de datos disjoint-set.
        x (int): El primer nodo.
        y (int): El segundo nodo.
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
        Arbol de recubrimiento minimo con kruskal

        Returns:
        list[tuple[int, int, int]]: Las aristas del árbol de expansión mínimo.
        """
        mst = []

        # se utiliza parent y rank para llevar el registro de los conjuntos 
        # y los representantes de cada conjunto para poder evitar ciclos
        parent = [i for i in range(len(self.nodes))]
        rank = [0] * len(self.nodes)

        self.edges = sorted(self.edges, key=lambda item: item[2])

        for u, v, w in self.edges:
            x = self.find(parent, self.node_to_index[u])
            y = self.find(parent, self.node_to_index[v])

            if x != y:
                mst.append((u, v, w))
                self.union(parent, rank, x, y)

        return mst
    



if __name__ == '__main__':

    # Guarda los resultados por grafo
    results = []

    # Leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        content = f.read()  
        sections = [section.strip() for section in content.split('\n\n') if section.strip()] 

    for section in sections:
        lines = section.splitlines()
        nodes = list(map(int, lines[0].split()))
        m = int(lines[1])

        edges = []
        for i in range(2, 2 + m):
            a, b, c = map(int, lines[i].split())
            edges.append((a, b, c))

        graph = Graph(nodes, edges)

        # Correr algoritmo de Kruskal
        mst = graph.kruskal()

        # Guardar resultados
        results.append((len(mst), mst))

        print(len(mst))
        for a, b, c in mst:
            print(a,b,c)


    # Escribir resultados en archivo out
    with open(sys.argv[2], 'w') as f:
        for length, mst in results:
            f.write(f"{length}\n")  
            for a, b, c in mst:
                f.write(f"{a} {b} {c}\n") 
            f.write("\n")
