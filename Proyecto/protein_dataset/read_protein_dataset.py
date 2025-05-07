
def load_protein_dataset(data_path):

    with open(data_path, 'r') as file:
        lines = file.readlines()

    i = 0
    graphs = []
    edges = []
    labels = {}
    for line in lines:
        if line.startswith('v'):
            _, node, label = line.split()
            node = int(node)
            if node not in labels:
                labels[node] = int(label)

        elif line.startswith('e'):
            _, node1, node2, _ = line.split()
            edges.append((int(node1), int(node2)))

        else:
            graphs.append([edges, labels])
            # print(F'ADDING GRAPH {i}')
            if i == 6:
                print([edges, labels])
            edges = []
            labels = {}
            i+= 1

    # print("Graphs loaded:", len(graphs))
    # print("First graph:", graphs[1])
    return graphs[1:]
        