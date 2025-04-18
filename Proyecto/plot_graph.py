import networkx as nx
import sys
from tests import read_graph
import matplotlib.pyplot as plt

if __name__=='__main__':
    input_path=sys.argv[1]

    nodes,edges,lables=read_graph(input_path)

    G=nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.draw(G)

    plt.show()


