# Escoger arbitrariamente un eje, incluir el vértice de mayor grado de los dos vértices conectados por el eje, descartar todos los demás ejes conectados por el vértice escogido y repetir hasta que no queden ejes.
import random

def solve(edges:list) -> list:
    sol = []

    # Initialize - save degrees and neighbours
    neighbours = {}
    degrees = {}

    for edge in edges:
        v1,v2 = edge

        if v1 not in neighbours:
            neighbours[v1] = set()
        neighbours[v1].add(v2)
        if v2 not in neighbours:
            neighbours[v2] = set()
        neighbours[v2].add(v1)

        if v1 not in degrees:
            degrees[v1] = 0
        degrees[v1] += 1
        if v2 not in degrees:
            degrees[v2] = 0
        degrees[v2] += 1


    while edges:
        edge = random.choice(edges)
        v1, v2 = edge

        vertex_max_degree = [v1,v2][[degrees[v1], degrees[v2]].index(max([degrees[v1], degrees[v2]]))]

        print("Edges: ", edges)
        print("Selected edge: ", edge)
        print("Current degrees of all vertices: ", degrees)
        print("Current neighbours of all vertices: ", neighbours)
        print("Vertex with maximum degree: ", vertex_max_degree)

        # update neighbours and degrees and delete edge
        for neighbour in neighbours[vertex_max_degree]:

            edge_neigh = tuple(sorted((vertex_max_degree, neighbour)))
            edges.remove(edge_neigh)

            neighbours[neighbour].remove(vertex_max_degree)
            degrees[neighbour] -= 1

        degrees[vertex_max_degree] = -1
        neighbours[vertex_max_degree] = set()

        sol.append(vertex_max_degree)

    return sol

# TODO: add main

edges = [(1,2),(2,3),(3,4),(2,4),(2,5)]
print(solve(edges))