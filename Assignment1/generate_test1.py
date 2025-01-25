import sys
import random




if __name__=='__main__':
    n=int(sys.argv[1])
    m=int(sys.argv[2])
    save_path=sys.argv[3]

    with open(save_path,'w') as f:
        for i in range(n):
            f.write(str(i)+' ')

        f.write('\n')
        f.write(str(m)+'\n')

        for i in range(m):
            a=random.randint(0,n-1)
            b=random.randint(0,n-1)

            f.write(str(a)+' '+str(b)+'\n')



