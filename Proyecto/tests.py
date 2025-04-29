import sys
import my_vf2pp
import networkx as nx


def read_graph(path):
    with open(path) as f:
        n_nodes=int(f.readline())

        line=f.readline()
        edges=[]
        while line:
            line=line.split()
            line=map(int,line)
            line=tuple(line)

            if line[0]==line[1]:
                continue

            edges.append(line)
            line=f.readline()

    return list(range(n_nodes)),edges,{i:0 for i in range(n_nodes)}




if __name__=='__main__':
    path_S=sys.argv[1]
    path_G=sys.argv[2]

    S=my_vf2pp.graph(*read_graph(path_S))
    G=my_vf2pp.graph(*read_graph(path_G))

    print(my_vf2pp.vf2pp(S,G))

    S_nx=nx.Graph()
    S_nx.add_edges_from(S.edges)

    G_nx=nx.Graph()
    G_nx.add_edges_from(G.edges)

    G_M=nx.algorithms.isomorphism.GraphMatcher(G_nx,S_nx)
    print(G_M.subgraph_is_isomorphic())


    