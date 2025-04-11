import sys
import eje1
import eje2 
import eje3
import eje4

def read_file(file):
    """
    Lee un archivo y extrae aristas de él. Cada arista se representa como una tupla de dos enteros.
    
    Parámetros:
    file (str): La ruta al archivo a leer.
    
    Retorna:
    list: Una lista de aristas, donde cada arista es una tupla de dos enteros.
    """
    edges = []
    with open(file) as f:
        line = f.readline()
        line = line.split()

        # Líneas con 2 elementos representan aristas
        while len(line) == 2:
            line = map(int, line)
            edges.append(tuple(line))

            line = f.readline()
            line = line.split()

    return edges


if __name__=='__main__':

    file=sys.argv[1]
    algo = sys.argv[2]
    assert 1 <= int(algo) <= 4, "El algoritmo debe ser un número entre 1 y 4"

    edges=read_file(file)

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


