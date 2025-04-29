
from protein_dataset.read_protein_dataset import load_protein_dataset

import networkx as nx
import my_vf2pp
import algoritmo_genetico
import vf2pp_fingerprints

import time

import pandas as pd

import itertools

graphs=load_protein_dataset('protein_dataset/truncated_dataset.txt')

datos=pd.DataFrame(columns=['algorithm','S_n_nodes','S_n_edges','G_n_nodes','G_n_edges','time','found_mapping'])


for S,G in itertools.permutations(graphs,2):
    print('label values are subset',set(S[1].values()).issubset(set(G[1].values())))
    print('S valid nodes',set(itertools.chain.from_iterable(S[0]))==set(S[1].keys()))
    print('G valid nodes',set(itertools.chain.from_iterable(G[0]))==set(G[1].keys()))

    #-------------------------------
    #sacar datos de networkx

    try:
        start=time.time()
        S_nx=nx.Graph()
        S_nx.add_edges_from(S[0])

        G_nx=nx.Graph()
        G_nx.add_edges_from(G[0])

        #toca hacer algo para poder meterle labels a networkx

        GM=nx.algorithms.isomorphism.GraphMatcher(G_nx,S_nx)
        ans=GM.subgraph_is_isomorphic()

        end=time.time()
        resultados=pd.DataFrame([['nx_vf2++',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans]],columns=datos.columns)

        datos=pd.concat((datos,resultados),ignore_index=True)
    except:
        pass
    #---------------------------------------------
    #sacar datos de my_vf2pp
    start=time.time()
    G_own=my_vf2pp.graph(list(G[1].keys()),G[0],G[1])
    S_own=my_vf2pp.graph(list(S[1].keys()),S[0],S[1])

    ans=(len(my_vf2pp.vf2pp(S_own,G_own))==len(S_own.nodes))

    end=time.time()
    resultados=pd.DataFrame([['our_vf2++',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans]],columns=datos.columns)

    datos=pd.concat((datos,resultados),ignore_index=True)
    #-------------------------------------------
    #sacar datos de algoritmo genetico

    

    #-----------------------

    #sacar datos de vf2pp_fingerprints
    try:
        start=time.time()
        G_own=vf2pp_fingerprints.Graph(list(G[1].keys()),G[0],G[1])
        S_own=vf2pp_fingerprints.Graph(list(S[1].keys()),S[0],S[1])

        vf2pp_fingerprints.associate_fingerprints(S_own,G_own)

        ans=ans=(len(my_vf2pp.vf2pp(S_own,G_own))==len(S_own.nodes))
        
        end=time.time()
        resultados=pd.DataFrame([['our_vf2++_fingerprints',len(S[1]),len(S[0]),len(G[1]),len(G[0]),end-start,ans]],columns=datos.columns)

        datos=pd.concat((datos,resultados),ignore_index=True)
    except:
        pass



print(datos.to_markdown())






    