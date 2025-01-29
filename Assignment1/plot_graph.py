from ejercicio1_final import FacebookNetwork
import sys



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

    G=FacebookNetwork(nodes,edges)

    G.draw_graph()


