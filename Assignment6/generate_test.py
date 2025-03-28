import random
import sys

def generate_edge(n):
    u=random.randrange(0,n)

    v=random.randrange(0,n)

    while v==u:
        v=random.randrange(0,n)

    return tuple(sorted((u,v)))


def generate(file,n,m,algo):
    m=min(m,(n*(n-1))//2)

    used_edges=set()
    with open(file,'w') as f:

        for i in range(m):
            edge=generate_edge(n)
            while edge in used_edges:
                edge=generate_edge(n)
            used_edges.add(edge)

            f.write(str(edge[0])+'\t'+str(edge[1])+'\n')
        f.write(str(algo))

    


if __name__=='__main__':
    output_file=sys.argv[1]
    n=int(sys.argv[2])
    m=int(sys.argv[3])

    algo=int(sys.argv[4])

    generate(output_file,n,m,algo)

