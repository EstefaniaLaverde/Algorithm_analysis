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
        for i in range(n):
            f.write(str(i)+' ')

        f.write('\n')
        f.write(str(m)+'\n')

        for i in range(m):
            a=random.randint(0,n-1)
            b=random.randint(0,n-1)
            c=random.randint(min_cost,max_cost)

            f.write(str(a)+' '+str(b)+' '+str(c)+'\n')