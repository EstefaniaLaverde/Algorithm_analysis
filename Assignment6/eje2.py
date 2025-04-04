# Escoger el vértice de mayor grado, descartar los ejes que llegan al vertice escogido y repetir hasta que no queden ejes.
import heapq

def solve(edges:set) -> list:

    sol = []

    # Initialize - save degrees and neighbours
    neighbours = {}
    degrees = {}
    heap = []

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

    # organize min heap
    for vertex, degree in degrees.items():
        heapq.heappush(heap, (-degree,vertex))

    while edges:
        vertex_max_degree = heapq.heappop(heap)[-1]

        # print("Vertex with maximum degree: ", vertex_max_degree)
        # print("Current degrees of all vertices: ", heap)
        # print("Current neighbours of all vertices: ", neighbours)

        neighbours_vertex_max_degrees = neighbours[vertex_max_degree]
        for neigh in neighbours_vertex_max_degrees:

            # Update degrees and neighbours 
            heap.remove((-degrees[neigh], neigh))
            degrees[neigh] += 1
            heapq.heappush(heap, (-degrees[neigh], neigh))

            neighbours[neigh].remove(vertex_max_degree)

            # Remove edge
            edge = tuple(sorted((neigh,vertex_max_degree)))
            edges.remove(edge)

        degrees[vertex_max_degree] = -1

        neighbours[vertex_max_degree] = set()
        sol.append(vertex_max_degree)

    return sol

# TODO: read tests 
# edges = {(1,2),(2,3),(3,4),(2,4),(2,5)}
# print(solve(edges))