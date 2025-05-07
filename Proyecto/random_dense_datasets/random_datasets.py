import random
import json
import math

def generate_edge(n):
    u=random.randrange(0,n)
    v=random.randrange(0,n)

    while v==u:
        v=random.randrange(0,n)

    return tuple(sorted((u,v)))


def generate(n,m):
    m=min(m,(n*(n-1))//2)

    used_edges=set()

    for i in range(m):
        edge=generate_edge(n)
        while edge in used_edges:
            edge=generate_edge(n)
        used_edges.add(edge)

        
    return list(used_edges)


if __name__=='__main__':
    n_samples=10
    min_n=9
    max_n=11
    min_density=0.97
    max_density=1


    save_path='random_dense_datasets/random_datasets_015.json'

    graphs=[]
    for i in range(n_samples):
        n=random.randint(min_n,max_n)

        n_pow=n**random.uniform(min_density,max_density)
        m=round(n_pow*(n_pow-1)/2)

        G=generate(n,m)

        labels={i:0 for i in range(n)}

        graphs.append([G,labels])

    with open(save_path,'w') as f:
        json.dump(graphs,f)


