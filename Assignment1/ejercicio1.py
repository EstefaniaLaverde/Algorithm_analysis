import sys
import os
from collections import deque


class graph:

    #nodes: list de enteros indicando los vertices
    #edges: lista de 2 tuplas indicando los ejes
    def __init__(self,nodes: list[int],edges: list[tuple[int,int]]):
        #self.nodes es un set en caso de que toque extender implementacion para agregar o eliminar nodos con eficiencia
        self.nodes=set(nodes)
        #self.edges es un map de nodos a conjuntos de vecinos, en caso de que toque extender implementacion para agregar o eliminar edges con eficiencia
        self.edges={node:set() for node in nodes}
        for a,b in edges:
            #los edges son bidireccionales asi se agregan en ambos mapas de vecinos
            self.edges[a].add(b)
            self.edges[b].add(a)


    #node: nodo desde donde se mide el radio
    #k: entero indicando la distancia maxima respecto a node
    #retorna true si y solo si existe un nodo a distancia mayor a k de central_node
    def node_radious_greater_than(self,central_node: int, k: int):

        #distancias de los nodos al nodo central, distancia -1 significa nodo no visitado
        distances={node:-1 for node in self.nodes}
        por_visi=deque()


        #inicilizamos nodo central como visitado y agregamos al queue de bsf
        por_visi.append(central_node)
        distances[central_node]=0
        while len(por_visi):
            node=por_visi.popleft()
            for neigh in self.edges[node]:
                
                #si se encuentra un nodo nuevo se actualiza distancia y se pone en que queue del bsf
                if distances[neigh]==-1:
                    distances[neigh]=distances[node]+1
                    por_visi.append(neigh)

                    #si se supera la cota de distancia retornamos true
                    if distances[neigh]>k:
                        return True

        return False

    def diameter_greater_than(self,k: int):
        #retorna si algun nodo tiene otro nodo a distancia mayor a k
        return any(self.node_radious_greater_than(node,k) for node in self.nodes)


    #determina si el grafo es conectado
    def is_connected(self):
        initial_node=next(iter(self.nodes),None)
        visited={node:False for node in self.nodes}
        por_visi=deque()

        por_visi.append(initial_node)
        visited[initial_node]=True

        while len(por_visi):
            node=por_visi.popleft()

            for neigh in self.edges[node]:
                if not visited[neigh]:
                    por_visi.append(neigh)
                    visited[neigh]=True

        return all(visited.values())


    

if __name__=='__main__':

    #leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b=map(int,f.readline().split())
            edges.append((a,b))


    G=graph(nodes,edges)

    k=6
    print((not G.diameter_greater_than(k)) and G.is_connected())



