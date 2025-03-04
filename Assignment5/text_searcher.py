import sys
import time

def arg_radix_sort(ranks):
    n=len(ranks)
    m=len(ranks[0])
    inds=list(range(n))

    #ordenamos las cordenadas de las tuplas desde la menos relevante a la mas relevante
    for j in range(m-1,-1,-1):

        #cargar buckets segun valores de la cordenada j
        buckets=[[] for i in range(n+1)]
        for i in range(n):
            buckets[ranks[inds[i]][j]].append(inds[i])

        #organizar indices segun cordenada j
        inds=[]
        for bucket in buckets:
            for val in bucket:
                inds.append(val)

    return inds

        
def argsort(a):
    values=zip(a,range(len(a)))
    values=sorted(values)
    inds=map(lambda x:x[1],values)
    return list(inds)
    




def suffix_array(text):
    n=len(text)

    #ordernar indices de sufijo a partir de la primera letra
    inds=argsort(text)
    #asignar rank segun la cantidad de letras distintas con una posicion menor segun el orden de indices
    rank=0
    ranks_merge=[[0,1] for i in range(n)]
    for i in range(1,n):
        if text[inds[i]]!=text[inds[i-1]]:
            rank+=1
        ranks_merge[inds[i]][0]=rank

    h=1
    while h<n:
        for i in range(n):
            if inds[i]+h<n:
                ranks_merge[inds[i]][1]=ranks_merge[inds[i]+h][0]+1
            else:
                ranks_merge[inds[i]][1]=0

        inds=arg_radix_sort(ranks_merge)

        rank=0
        ranks_merge[inds[0]][0]=0
        for i in range(1,n):
            if ranks_merge[inds[i]]!=ranks_merge[inds[i-1]]:
                rank+=1

            ranks_merge[inds[i]][0]=rank

        #se han ordenado completamente los indices
        if rank==n:
            return inds

        h=h*2

    return inds


def get_lower_bound_on_char(text,suff_arr,pattern,ind,l,r):
    n=len(text)
    while r-l>1:
        mid=(r+l)//2

        if suff_arr[mid]+ind<n:
            if text[suff_arr[mid]+ind]<pattern[ind]:
                l=mid
            else:
                r=mid

        else:
            l=mid

    if suff_arr[r]+ind<n:
        if text[suff_arr[r]+ind]<pattern[ind]:
            return r
        else:
            return l

    else:
        return r

def get_upper_bound_on_char(text,suff_arr,pattern,ind,l,r):
    n=len(text)
    while r-l>1:
        mid=(r+l)//2

        if suff_arr[mid]+ind<n:
            if pattern[ind]<text[suff_arr[mid]+ind]:
                r=mid
            else:
                l=mid

        else:
            r=mid

    if suff_arr[l]+ind<n:
        if pattern[ind]<text[suff_arr[l]+ind]:
            return l
        else:
            return r

    else:
        return r

def get_positions(text,suff_arr,pattern):
    m=len(pattern)
    n=len(text)

    l=0
    r=n-1

    for i in range(m):
        #hallar cotas superir e inferior
        l=get_lower_bound_on_char(text,suff_arr,pattern,i,l,r)
        r=get_upper_bound_on_char(text,suff_arr,pattern,i,l,r)

        #avanzar indices para hacer coincider primeros i caracteres
        l+=(suff_arr[l]+i>=n) or (text[suff_arr[l]+i]!=pattern[i])
        r-=(suff_arr[r]+i>=n) or (text[suff_arr[r]+i]!=pattern[i]) 

        if r<l:
            return []

    return suff_arr[l:r+1]


def solve_querys(text_file,query_file,output_path):
    with open(text_file) as f:
        text=f.read()

    with open(query_file) as f:
        querys=f.read()
    querys=querys.split('\n')

    start=time.time()
    position_results=[]
    suff_arr=suffix_array(text)
    for q in querys:
        position_results.append(get_positions(text,suff_arr,q))
    
    end=time.time()


    with open(output_path,'w') as f:
        for q,positions in zip(querys,position_results):
            f.write(q)
            for p in positions:
                f.write('\t'+str(p))
            f.write('\n')

    return end-start



    

if __name__=='__main__':
    #text_file=sys.argv[1]
    #query_file=sys.argv[2]
    #output_path=sys.argv[3]    


    text='naaaanaaannaaa'
    pattern='naaan'

    suff_arr=suffix_array(text)

    print(get_positions(text,suff_arr,pattern))



    """with open('tests/text_file_1000000.txt')as f:
        text=f.read()

    print('loaed file')

    start=time.time()
    suff_arr=suffix_array(text)
    end=time.time()

    print(end-start)"""