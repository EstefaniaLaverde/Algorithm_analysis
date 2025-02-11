import random
import os
import sys

def generate_edge(n):
    a=random.randint(0,n-1)
    b=random.randint(0,n-1)
    while a==b:
        b=random.randint(0,n-1)
        
    return (a,b)


if __name__=='__main__':
    n=int(sys.argv[1])
    m=int(sys.argv[2])
    min_cost=int(sys.argv[3])
    max_cost=int(sys.argv[4])


    save_path=sys.argv[5]
    with open(save_path,'w') as f:
        f.write(str(n)+'\n')


        found_edges=set()
        for i in range(m):
            a,b=generate_edge(n)
            c=random.randint(min_cost,max_cost)

            #verificar no se generan ejes repetidos
            while (min(a,b),max(a,b)) in found_edges:
                a,b=generate_edge(n)
            found_edges.add((min(a,b),max(a,b)))

            f.write(str(a)+' '+str(b)+' '+str(c)+'\n')