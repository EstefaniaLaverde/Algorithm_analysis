
from collections import deque
import sys
import time


class graph:
    def __init__(self,n: int, edges: list[tuple[int,int,int]]):
        self.edges_out=[{} for i in range(n)]

        #para guardar que parejas de nodos ya tienen un eje entre ellos
        found_edges=set()
        for u,v,c in edges:
            self.edges_out[u][v]=c


            #sacar error si se ingresa un grafo con multiples edges entre el mismo par de nodos
            #sacamos minimo y maximo para tener representacion canonoca del eje (u,v) sin importor direccion
            (a,b)=(min(u,v),max(u,v))
            if (a,b) in found_edges:
                raise AssertionError("el grafo tiene multiples edges para un mismo par de nodos")
            found_edges.add((a,b))


    #retorna una lista de nodos que representa el camino entre src_node y target_node en el grafo
    #retorna lista vacia en caso de que no haya camino
    def get_path(self,src_node,target_node):
        n=len(self.edges_out)

        #lista que apunta al padre en el bsf para poder reconstruir camino de la busqueda
        #-1 significa que el nodo no ha sido visitado
        father=[-1 for i in range(n)]
        por_visi=deque()

        #marcador para el nodo fuente, es el unico nodo que es su propio padre
        father[src_node]=src_node
        por_visi.append(src_node)

        while len(por_visi):
            node=por_visi.popleft()

            #reconstruir camino
            if node==target_node:
                path=[]
                while father[node]!=node:
                    path.append(node)
                    node=father[node]
                path.append(node)

                path.reverse()
                return path

            for neigh in self.edges_out[node]:
                #solo transitamos edges con peso mayor a 0 y hacia nodos no visitados
                if (self.edges_out[node][neigh]>0) and (father[neigh]==-1):
                    por_visi.append(neigh)
                    father[neigh]=node
        
        return []


    def edmond_karps(self):
        n=len(self.edges_out)

        #variable para guardar la capacidad maxima de un edge en el grafo
        max_cap=0
        #create residual graph
        residual=graph(n,[])
        for u in range(n):
            for v in self.edges_out[u]:
                c=self.edges_out[u][v]
                residual.edges_out[u][v]=c
                residual.edges_out[v][u]=0
                max_cap=max(max_cap,c)

        src_node=0
        sink_node=n-1
        
        while True:
            path=residual.get_path(src_node,sink_node)
            if len(path):
                #determinar cuanto flujo se puede agregar por ese camino
                min_res_on_path=max_cap
                for i in range(len(path)-1):
                    min_res_on_path=min(min_res_on_path,residual.edges_out[path[i]][path[i+1]])
                

                #agregar flujo por el camino
                for i in range(len(path)-1):
                    u=path[i]
                    v=path[i+1]

                    #obtener capacidad del edge en el grafo original
                    if v in self.edges_out[u]:
                        edge_capacity=self.edges_out[u][v]
                    else:
                        edge_capacity=self.edges_out[v][u]

                    #actualizar flujo en el residual
                    residual.edges_out[u][v]-=min_res_on_path
                    residual.edges_out[v][u]=edge_capacity-residual.edges_out[u][v]
                    
            else:
                break


        #crear lista con flujos en el formato definido
        edges_flow=[]
        for u in range(n):
            for v in self.edges_out[u]:
                #el residuo es el espacio sobrante, asi con la resta obtenemos el espacio ocupado
                edges_flow.append((u,v,self.edges_out[u][v]-residual.edges_out[u][v]))

        #sacar flujo total, medimos el flujo que sale de la fuente
        total_flow=0
        for edge in edges_flow:
            if edge[0]==src_node:
                total_flow+=edge[2]

        return edges_flow,total_flow



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



    G=graph(n,edges)

    #medir tiempo ejecucion de edmond_karps
    start=time.time()
    edges_flow,total_flow=G.edmond_karps()
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



