# OSM Graph Nodes and Edges Extraction

## Description
This Python script extracts the street network of a specified municipality from OpenStreetMap (OSM), relabels the nodes with sequential IDs, labels the edges as one-way or two-way, and generates both a network graph visualization and an interactive map.

The script performs the following steps:

1. Downloads the street network of a specified area using `osmnx`.
2. Extracts node coordinates and relabels node IDs sequentially.
3. Extracts edge information, relabels node IDs in the edges, and creates a labeled edge list:
   - `1` for one-way streets
   - `0` for two-way streets
4. Saves nodes and edges as CSV files:
   - `1_nodes_renamed.csv` — relabeled nodes
   - `2_edges_labeled.csv` — labeled edges
5. Generates a static **NetworkX graph** with node positions.
6. Generates an **interactive Folium map** with numbered nodes (`map.html`).

---

## Requirements

- Python 3.8+
- Packages:
  ```bash
  pip install osmnx pandas networkx matplotlib folium
