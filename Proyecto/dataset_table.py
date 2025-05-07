import os
import json
import numpy as np
import pandas as pd


def process_dataset(file_path: str, dataset_name: str) -> dict:
    """
    Reads a TXT dataset in gSpan ‘t / v / e’ format *or* the new JSON format
    and returns the same statistics dictionary your LaTeX table expects.
    """
    graphs = []
    #for the txt files

    if file_path.lower().endswith(".txt"):
        with open(file_path, "r") as file:
            current = {"vertices": set(), "edges": [], "labels": set()}
            for line in file:
                if line.startswith("t"):
                    if current["vertices"]:
                        graphs.append(current)
                        current = {"vertices": set(), "edges": [], "labels": set()}
                elif line.startswith("v"):
                    _, vid, label = line.strip().split()
                    current["vertices"].add(int(vid))
                    current["labels"].add(int(label))
                elif line.startswith("e"):
                    _, src, dst, label = line.strip().split()
                    current["edges"].append((int(src), int(dst)))
                    current["labels"].add(int(label))
            if current["vertices"]:
                graphs.append(current)

    # for the json files
    else:  # assume .json
        with open(file_path, "r") as file:
            data = json.load(file)

        for entry in data:

            if isinstance(entry, dict):
                edges = entry["edges"]
                lbls = entry["labels"]
            else:
                edges, lbls = entry

            vertices = set()
            edges_list = []
            labels = set()

            for src, dst in edges:
                src, dst = int(src), int(dst)
                vertices.update([src, dst])
                edges_list.append((src, dst))

            for v, lab in lbls.items():
                vertices.add(int(v))
                labels.add(int(lab))

            graphs.append({"vertices": vertices, "edges": edges_list, "labels": labels})

    #  statistics 
    vertex_counts = [len(g["vertices"]) for g in graphs]
    edge_counts = [len(g["edges"]) for g in graphs]

    degrees = []
    for g in graphs:
        deg = {v: 0 for v in g["vertices"]}
        for src, dst in g["edges"]:
            deg[src] += 1
            deg[dst] += 1
        degrees.append(list(deg.values()))

    degree_averages = [np.mean(d) for d in degrees]
    degree_stds = [np.std(d) for d in degrees]
    label_counts = [len(g["labels"]) for g in graphs]

    return {
        "": dataset_name,
        "Min Vertices": np.min(vertex_counts),
        "Min Edges": np.min(edge_counts),
        "Max Vertices": np.max(vertex_counts),
        "Max Edges": np.max(edge_counts),
        "Avg (SD) Vertices": f"{np.mean(vertex_counts):.1f} ({np.std(vertex_counts):.2f})",
        "Avg (SD) Edges": f"{np.mean(edge_counts):.1f} ({np.std(edge_counts):.2f})",
        "Avg (SD) Degree": f"{np.mean(degree_averages):.2f} ({np.mean(degree_stds):.2f})",
        "Total Labels": len(set().union(*[g["labels"] for g in graphs])),
        "Avg (SD) Labels": f"{np.mean(label_counts):.2f} ({np.std(label_counts):.2f})",
    }



mutag_stats = process_dataset(
    "biological_datasets/mutag.txt", "MUTAG\nSmall Sparse"
)
proteins_stats = process_dataset(
    "protein_dataset/proteins_original_data.txt", "PROTEINS\nMedium Sparse"
)
random_dense_stats = process_dataset(
    "random_dense_datasets/random_datasets_015.json", "RANDOM\nDense"
)

df = pd.DataFrame([mutag_stats, proteins_stats, random_dense_stats])

latex_table = df.to_latex(
    index=False,
    caption="Statistics of the MUTAG, PROTEINS and RANDOM datasets.",
    label="tab:dataset_stats",
    column_format="lccccccccc",
    escape=False,
)

print(latex_table)
