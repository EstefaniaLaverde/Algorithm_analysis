import sys
import eje1
import eje2 
import eje3
import eje4

def read_file(file):
    edges=[]
    with open(file) as f:
        line=f.readline()
        line=line.split()

        #lineas de 2 elmeentos tienen edges
        while len(line)==2:
            line=map(int,line)
            edges.append(tuple(line))

            line=f.readline()
            line=line.split()

        #ultima linea de un elemento tiene el algoritmo a usar
        algo=int(line[0])

    return edges,algo


if __name__=='__main__':

    file=sys.argv[1]

    edges,algo=read_file(file)

    if algo==1:
        cover=eje1.solve(edges)
    elif algo==2:
        cover=eje2.solve(edges)
    elif algo==3:
        cover=eje3.solve(edges)
    else:
        cover=eje4.solve(edges)

    print(cover)
    print(len(cover))


