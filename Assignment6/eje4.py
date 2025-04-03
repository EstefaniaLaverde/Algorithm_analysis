import random
from typing import Iterable

#contenedor que permite operaciones de seleccion aleatoria con dist uniforme y eliminacion eficiente
class random_selectable_set:
    def __init__(self,values:Iterable):
        self.values=list(values)
        self.values_position={val:i for i,val in enumerate(self.values)}


    def get_random_val(self):
        return random.choice(self.values)

    def remove(self,element):
        if element not in self.values_position:
            return

        #remover de values_set es facil
        #para remover de values, intercambiamos el elemento a eliminar con el de la ultima posicion para eliminar de forma eficiente


        element_pos=self.values_position[element]
        last_element=self.values[-1]

        self.values[-1],self.values[element_pos]=self.values[element_pos],self.values[-1]
        self.values_position[element],self.values_position[last_element]=self.values_position[last_element],self.values_position[element]

        self.values.pop()
        self.values_position.pop(element)

    def add(self,element):
        self.values.append(element)
        self.values_positions[element]=len(self.values)-1

    def __contains__(self,element):
        return element in self.values_position

    def __len__(self):
        return len(self.values)



def solve(edges):
    neighs={}

    #ordernar cordenadas de los edges para representacion canonica
    edges=map(lambda x: tuple(sorted(x)), edges)
    edges=list(edges)

    #crear conjuntos de vecinos
    for u,v in edges:
        if u not in neighs:
            neighs[u]=set()
        neighs[u].add(v)

        if v not in neighs:
            neighs[v]=set()
        neighs[v].add(u)


    edges=random_selectable_set(edges)
    cover=[]
    while len(edges):
        #obtener eje aleatorio
        edge=edges.get_random_val()

        #obtener nodo aleatorio
        node=random.choice(edge)

        cover.append(node)

        #quitar edges que usan a node
        for neigh in neighs[node]:
            edge=tuple(sorted((node,neigh)))
            if edge in edges:
                edges.remove(edge)
            neighs[neigh].remove(node)
        neighs[node].clear()


    return cover