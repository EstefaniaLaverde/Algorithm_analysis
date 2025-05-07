
def read_dataset(dataset_path):
    """
    Reads a dataset from a given path and returns the data.
    :param dataset_path: Path to the dataset file.
    :return: Data read from the dataset.
    """

    with open(dataset_path, 'r') as file:
        lines = file.readlines()

    atom_labels = ['C', 'N', 'O', 'F', 'I', 'Cl', 'Br']

    graphs = []
    edges = []
    labels = {}
    for line in lines:
        if line.startswith('v'):
            _, node, label = line.split()
            node = int(node)

            if node not in labels:
                labels[node] = atom_labels[int(label)]

        elif line.startswith('e'):
            _, node1, node2, number_of_links = line.split()
            edges.add(((int(node1), int(node2)), int(number_of_links)))

        else:
            graphs.append([list(edges), labels])
            edges = set()
            labels = {}

    return graphs[1:]  # Skip the first graph as it is empty

def process_graphs(graphs):
    processed_graphs = []
    for i, graph in enumerate(graphs):
        new_edges = []

        edges, labels = graph
        added_node_ini = len(labels) +1
        for edge in edges:
            edge, number_of_links = edge
            v1, v2 = edge
            if number_of_links >= 1:
                new_edges.append(edge)
                # Process the edge with multiple links
                for _ in range(number_of_links):
                    # Add a new node and link it to the existing nodes
                    labels[added_node_ini] = 'Extra'
                    new_edges.append((v1, added_node_ini))  
                    new_edges.append((v2, added_node_ini))
                    added_node_ini += 1
            
            else: new_edges.append(edge)
        processed_graphs.append((new_edges, labels))
        
    return processed_graphs

def read_and_process_dataset(dataset_path):
    """
    Reads and processes a dataset from a given path.
    :param dataset_path: Path to the dataset file.
    :return: Processed graphs.
    """
    graphs = read_dataset(dataset_path)
    processed_graphs = process_graphs(graphs)
    return processed_graphs

# print("Graphs loaded:", len(graphs))
# print("First graph:", graphs[0])
# print("First graph processed:", process_graphs(graphs)[0])

# # save the processed graphs to a file
# with open('processed_graphs.txt', 'w') as f:
#     for graph in process_graphs(graphs):
#         edges, labels = graph
#         f.write("Edges:\n")
#         for edge in edges:
#             f.write(f"{edge}\n")
#         f.write("Labels:\n")
#         for node, label in labels.items():
#             f.write(f"{node}: {label}\n")
#         f.write("\n")  # Separate graphs with a newline
        
