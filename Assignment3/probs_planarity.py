import random
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import pandas as pd


def generate_edge(n):
    a=random.randint(0,n-1)
    b=random.randint(0,n-1)
    while a==b:
        b=random.randint(0,n-1)

    return (min(a,b),max(a,b))

def generate_edges(n,m):
    used_edges=set()

    m=min(m,(n*(n-1))//2)

    while len(used_edges)<m:
        a,b=generate_edge(n)
        if (a,b) not in used_edges:
            used_edges.add((a,b))
    
    return list(used_edges)

def generate_graph(n,m):
    G=nx.Graph()

    G.add_nodes_from(range(n))

    edges=generate_edges(n,m)
    G.add_edges_from(edges)

    return G


def planarity_experiment(n,attempts):
    max_edges=3*n-6
    probs=[]
    for edge_count in range(max_edges+1):
        planar_count=0
        for i in range(attempts):
            G=generate_graph(n,edge_count)
            planar_count+=nx.is_planar(G)

        probs.append(planar_count/attempts)

    return probs


def save_graph_to_xlsx(G,output_path):
    df=pd.DataFrame(G.edges,columns=['node1','node2'])
    df.to_excel(output_path)

if __name__=='__main__':
    n=20
    max_edges=3*n-6
    attempts=1000

    probs=planarity_experiment(n,attempts)

    plt.plot(list(range(max_edges+1)),probs)
    plt.show()


