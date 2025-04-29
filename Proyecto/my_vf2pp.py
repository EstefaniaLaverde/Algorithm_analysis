from collections import deque
import itertools

class graph:

    def __init__(self,nodes,edges,labels):
        self.nodes=set(nodes)
        self.neighs={node:set() for node in nodes}
        self.labels=labels

        for u,v in edges:
            self.neighs[u].add(v)
            self.neighs[v].add(u)


    #funcion de vecindad respecto al mapeo como en el paper
    #sacada de 3.3.1 del paper
    def T1(self,m):
        V1=set(m.keys())
        candidates=self.nodes.difference(V1)
        neighbors=filter(lambda x: len(self.neighs[x].intersection(V1))!=0,candidates)
        return set(neighbors)


    def T2(self,m):
        V2=set(m.values())
        candidates=self.nodes.difference(V2)
        neighbors=filter(lambda x: len(self.neighs[x].intersection(V2))!=0,candidates)
        return set(neighbors)


    def conn(self,H,u):
        return len(H.intersection(self.neighs[u]))

    def deg(self,u):
        return len(self.neighs[u])

    #bsf estandar
    def bsf(self,u):
        por_visi=deque()
        por_visi.append(u)

        depths={}
        depths[u]=0

        while por_visi:
            node=por_visi.popleft()

            for neigh in self.neighs[node]:
                if neigh not in depths:
                    por_visi.append(neigh)
                    depths[neigh]=depths[node]+1

        return depths

    #retorna lista de listas con los nodos en cada nivel del bsf
    def bsf_levels(self,u):
        depths=self.bsf(u)

        levels=[[] for i in range(max(depths.values())+1)]
        for u,d in depths.items():
            levels[d].append(u)

        return levels

    #retorna diccionario con frecuencias de cada label
    def get_l_counts(self):
        l_counts={}
        for node in self.nodes:
            if self.labels[node] not in l_counts:
                l_counts[self.labels[node]]=0
            l_counts[self.labels[node]]+=1
        return l_counts

    #obtener matching order
    #sacada de algorithm 2 y algorithm 3 del paper, en el paper vienen separadas pero las juntamos por simplicidad
    def matching_order(self,G_l_counts):
        M=[]
        M_set=set()

        #funciones definidas en el paper para el ordanmiento de nodos
        #note los valores estan por referencia, asi las funciones se actualizan automaticamente al cambiar los diccionarios o sets que refieren
        L=lambda x: self.labels[x]
        F_M=lambda x: G_l_counts[x]
        conn_M=lambda x: self.conn(M_set,x)


        while self.nodes.difference(M_set):
            roots=arg_max(self.deg,arg_min(compose(F_M,L),self.nodes.difference(M_set)))
            r=roots[0]
            levels=self.bsf_levels(r)

            for level in levels:
                level_set=set(level)
                #PROCESS LEVEL, algorithm 3 del paper

                while level_set:
                    ms=arg_min(compose(F_M,L),arg_max(self.deg,arg_max(conn_M,level_set)))
                    m=ms.pop()

                    M.append(m)
                    M_set.add(m)
                    level_set.remove(m)

                    #por definicion de F_M en 4.1.1
                    #al agregar un elemento a M debemos restar 1 en label del respectivo elemento
                    G_l_counts[self.labels[m]]-=1

        return M

    #obtener vecinos de u que tienen label l
    def gamma(self,l,u):
        ans=set()
        for neigh in self.neighs[u]:
            if self.labels[neigh]==l:
                ans.add(neigh)
        return ans

    #funcion de eliminar nodos
    def erase_node(self,u):
        if u in self.nodes:
            self.labels.pop(u)
            for v in self.neighs[u]:
                self.neighs[v].remove(u)
            self.neighs.pop(u)
            self.nodes.remove(u)
        



#funciones auxiliares para sacar arg min y composicion de funciones para sacar el matching order

def compose(f,g):
    return lambda x: f(g(x))

def arg_max(f,S):
    S=iter(S)

    val=next(S)

    best_vals=[val]
    best_f_val=f(val)

    for val in S:
        f_val=f(val)
        if f_val>best_f_val:
            best_f_val=f_val
            
        if f_val==best_f_val:
            best_vals.append(val)

    return best_vals

def arg_min(f,S):
    S=iter(S)

    val=next(S)

    best_vals=[val]
    best_f_val=f(val)

    for val in S:
        f_val=f(val)
        if f_val<best_f_val:
            best_f_val=f_val
            
        if f_val==best_f_val:
            best_vals.append(val)

    return best_vals

#funcion de consitencia intuida de 2.1.3 del paper
def check_consistency(f,S,G):

    V2=set(f.values())
    V1=set(f.key())

    if len(V1)!=len(V2):
        return False

    if (not V1.issubset(S.nodes)) or (not V2.issubset(G.nodes)):
        return False

    for node in f.keys():
        if S.label(node)!=G.label(node):
            return False

        for neigh in S.neighs[node].intersection(V1):
            if f[neigh] not in G.neighs[f[node]]:
                return False

    return True

#funcion de consistencia para extensiones, se asume el mapeo sin extension es consistente
#intuida de 2.1.3 del paper y de 3.4.2
def check_extension_consistency(u,v,f,S,G):
    V1=set(f.keys())
    V2=set(f.values())
    for neigh in S.neighs[u].intersection(V1):
        if f[neigh] not in G.neighs[v]:
            return False
    return True


#funcion de corte
#retorna booleano, los significadoes son los siguientes
#True: estoy seguro el mapeo actual no se puede extender a un mapeo completo
#False: no estoy seguro el mapeo actual se pueda o no extender a mapeo completo
def check_extension_cut(u,v,f,S,G):

    labels=itertools.chain(S.get_l_counts().keys(),G.get_l_counts().keys())
    for l in labels:
        if (len(G.gamma(l,v).intersection(G.T2(f)))<len(S.gamma(l,u).intersection(S.T1(f)))) or \
        (S.labels[u]!=G.labels[v]):
            return True
    return False
    


def vf2pp(S,G):
    f={}

    S_label_set=set(S.labels.values())
    nodes_to_erase=[]
    for u in G.nodes:
        if G.labels[u] not in S_label_set:
            nodes_to_erase.append(u)
    
    for u in nodes_to_erase:
        G.erase_node(u)

    G_l_counts=G.get_l_counts()
    
    M=S.matching_order(G_l_counts)

    return recu_vf2pp(M,f,S,G)


def recu_vf2pp(M,f,S,G):
    if len(f)==len(S.nodes):
        return f

    #seleccionar nodo decuerdo al matching order
    u=M[len(f)]

    #construccion de candidates deacuerdo a 5.3 del paper
    candi_neighs=set(f.keys()).intersection(S.neighs[u])
    if candi_neighs:
        u_p=candi_neighs.pop()
        candi_pairs=G.neighs[f[u_p]].difference(set(f.values()))
    else:
        candi_pairs=G.nodes.difference(set(f.values()))


    
    for v in candi_pairs:
        if check_extension_consistency(u,v,f,S,G) and (not check_extension_cut(u,v,f,S,G)):
            f[u]=v
            
            f=recu_vf2pp(M,f,S,G)

            if len(f)==len(S.nodes):
                return f

            f.pop(u)
    return f


if __name__=='__main__':
    

    #grafo "dibujo de casa"
    #es decir ciclo de 5 con una linea atravesada para que parezca una casa
    #"un cuadrado con un techo tringular"
    G=graph(list(range(5)),
            [(0,1),(1,2),(2,3),(3,4),(4,0),(4,1)],
            {i:0 for i in range(5)})

    #hallar cuadrado "base" de la casa
    #ciclo de 4
    S=graph(list(range(4)),
            [(0,1),(1,2),(2,3),(3,0)],
            {i:0 for i in range(4)})
    print(vf2pp(S,G))


    #hallar el tringulo "techo" de la casa
    #grafo ciclo de 3 triangulo
    S2=graph(list(range(3)),
            [(0,1),(1,2),(2,0)],
            {i:0 for i in range(3)})

    print(vf2pp(S2,G))


    