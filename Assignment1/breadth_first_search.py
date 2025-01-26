from typing import Optional
from random import choice
import sys

class Queue():
    def __init__(self) -> None:
        self.queue = []
        self.front = None
        self.rear = None

    def is_empty(self) -> bool:
        return self.queue == []

    def enqueue(self, element: int) -> None:
        self.queue = [element] + self.queue
        self.front = self.queue[-1]
        self.rear = self.queue[0]

    def dequeue(self) -> Optional[int]:
        if self.is_empty(): return None

        front = self.front
        self.queue = self.queue[:-1]
        if self.is_empty():
            self.front = None
            self.rear = None
        else:
            self.front = self.queue[-1]
            self.rear = self.queue[0]

        return front

class Graph():
    def __init__(self, nodes: list[int], edges: list[list[int]]) -> None:
        self.nodes = nodes
        self.edges = edges

    def neighbours(self, node:int) -> list[int]:
        assert (node in self.nodes), 'The node does not exist in the graph'

        neighbours = []
        for edge in self.edges:
            e = edge.copy()
            if node in e:
                e.remove(node)
                neighbours.append(e[0])

        return list(set(neighbours))

    def bfs_modified(self, root: int, objective_node: int, max_steps:int = 6) -> bool:

        assert (root in self.nodes), 'The root node does not exist in the graph'

        assert (objective_node in self.nodes), 'The objective node does not exist in the graph'

        queue = Queue()
        visited = set()
        steps = 0

        queue.enqueue(root)
        visited.add(root)

        while not queue.is_empty():
            node = queue.dequeue()

            if steps > max_steps:
                return False

            if node == objective_node:
                return True
            
            prev_visited = visited.copy()
            for neighbour in self.neighbours(node):
                if neighbour not in visited:
                    queue.enqueue(neighbour)
                    visited.add(neighbour)
                
            if visited != prev_visited:
                steps += 1
            
        return False

    def check_6degrees(self) -> bool:
        checked_nodes = []

        for node in self.nodes:
            need_to_check = [n for n in self.nodes if n!=node and n not in checked_nodes]

            for check_node in need_to_check:
                if self.bfs_modified(node, check_node) == False:
                    return False
                
            checked_nodes.append(node)
        return True

    def check_6degrees2(self, max_steps:int = 6) -> bool:
        assert (self.nodes), 'There are no nodes in the graph'

        root = choice(list(self.nodes))

        queue = Queue()
        visited = set()
        steps = 0

        queue.enqueue(root)
        visited.add(root)

        while not queue.is_empty():
            node = queue.dequeue()

            prev_visited = visited.copy()
            for neighbour in self.neighbours(node):
                if neighbour not in visited:
                    queue.enqueue(neighbour)
                    visited.add(neighbour)

            if prev_visited != visited:
                steps += 1

            if len(visited) == len(set(self.nodes)) and steps <= max_steps:
                return True
            elif steps > max_steps:
                return False
            
        return False

            
    ## LA FUNCION DE GRAFICACION HECHA CON GPT
    def draw_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.edges)

        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()
    

if __name__=='__main__':
    input_path=sys.argv[1]

    #leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b=map(int,f.readline().split())
            edges.append([a,b])

    G=Graph(nodes,edges)

    print(G.check_6degrees2())