import sys
import numpy as np


if __name__=='__main__':

    #leer grafo desde un archivo txt con el formato especificado
    with open(sys.argv[1]) as f:
        nodes=list(map(int,f.readline().split()))
        m=int(f.readline())

        edges=[]
        for i in range(m):
            a,b=map(int,f.readline().split())
            edges.append((a,b))

    #diccionario de reenumeracion de nodos para matriz de adyacencia
    node_to_ind={node:i for i,node in enumerate(nodes)}
    A=np.eye(len(nodes))

    for x,y in edges:
        A[node_to_ind[x],node_to_ind[y]]=1
        A[node_to_ind[y],node_to_ind[x]]=1

    k=6

    A_k=np.linalg.matrix_power(A,k)

    print(A_k.min()>1/2)
