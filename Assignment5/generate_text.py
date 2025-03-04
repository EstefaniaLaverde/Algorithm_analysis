import random
import sys

max_query_size=12
letters=[chr(i+ord('a')) for i in range(ord('z')-ord('a')+1)]
sings=[' ','\n','.',',',':']
alphabet=letters


def generate_text_file(text_file,n):
    with open(text_file,'w') as f:
        for i in range(n):
            f.write(random.choice(alphabet))

    

def generate_query_file(query_file,m):
    with open(query_file,'w') as f:
        for i in range(m):
            query_size=random.randint(1,max_query_size)
            for j in range(query_size):
                f.write(random.choice(letters))
            f.write('\n')

    

if __name__=='__main__':

    text_file=sys.argv[1]
    n=sys.argv[2]

    query_file=sys.argv[3]
    m=sys.argv[4]

    generate_files(text_file,n)
    generate_query_file(query_file,m)


    


    

    

