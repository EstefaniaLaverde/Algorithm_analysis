import networkx as nx
import matplotlib.pyplot as plt
import csv
import sys

def plot_planar_graph_from_csv(csv_file):
    G = nx.Graph()
    
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            source = int(row['node1'])
            target = int(row['node2'])
            G.add_edge(source, target)
    
    is_planar, embedding = nx.check_planarity(G)
    if not is_planar:
        print("The graph is not planar and cannot be drawn without crossing edges.")
        return

    pos = nx.planar_layout(G)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            edge_color='gray', node_size=800, font_size=12)
    plt.title("Planar Graph")
    plt.show()

if __name__ == '__main__':
    csv_file = "C:/Users/pablo/OneDrive/Documents/Universidad/Dalgo2/Algorithm_analysis/Assignment3/graphs/planar_40_60.csv"
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    plot_planar_graph_from_csv(csv_file)
