def solve(edges):
    neighs={}

    #ordernar cordenadas de los edges para representacion canonica
    edges=map(lambda x: tuple(sorted(x)), edges)
    #edges es un set para despues quitarle elementos facilmente
    edges=set(edges)

    #crear conjuntos de vecinos
    for u,v in edges:
        if u not in neighs:
            neighs[u]=set()
        neighs[u].add(v)

        if v not in neighs:
            neighs[v]=set()
        neighs[v].add(u)


    cover=[]


    while len(edges):
        #obtener edge arbitrario
        u,v=edges.pop()

        #agregar nodos del edge al cover
        cover.append(u)
        cover.append(v)

        #quitar edges que usan a u
        for neigh in neighs[u]:
            edge=tuple(sorted((u,neigh)))
            if edge in edges:
                edges.remove(edge)
            neighs[neigh].remove(u)
        neighs[u].clear()

        #quitar edges que usan a v
        for neigh in neighs[v]:
            edge=tuple(sorted((v,neigh)))
            if edge in edges:
                edges.remove(edge)
            neighs[neigh].remove(v)
        neighs[v].clear()

    return cover



        


        