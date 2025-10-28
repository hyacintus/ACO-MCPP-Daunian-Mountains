# Relabel Nodes and Highlight Duplicate Edges

## Description
This Python script processes a filtered street network by:

1. Removing edges labeled as `1`.
2. Relabeling the node IDs sequentially starting from 1.
3. Updating the edge data to reflect the new node IDs.
4. Creating a NetworkX graph of the filtered network.
5. Identifying duplicate edges and highlighting them in red.
6. Generating a static visualization with Matplotlib.
7. Creating an interactive Folium map showing all nodes.

The script is intended to help visualize duplicate edges and clean the network data after filtering.

---

## Requirements

- Python 3.8+
- Packages:
  ```bash
  pip install pandas networkx matplotlib folium
