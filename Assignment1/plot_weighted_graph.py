from ejercicio5_final import Graph
import sys


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

    graph.draw_graph()