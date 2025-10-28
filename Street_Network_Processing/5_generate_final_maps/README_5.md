# Generate Final Street Network Maps

## Description
This Python script finalizes the street network data by:

1. Loading the updated nodes and edges from previous steps (`5_nodes.csv` and `5_edges.csv`).
2. Optionally checking for nodes that are not connected to any edge (commented out by default).
3. Duplicating edges with `label = 0` to create bidirectional connections.
4. Saving the processed nodes and edges as Excel (`6_nodes.xlsx`, `6_edges.xlsx`) and CSV (`6_nodes.csv`, `6_edges.csv`) files.
5. Generating a NetworkX graph, with edges of `label = 1` highlighted in red.
6. Creating interactive Folium maps:
   - `updated_map.html` for all nodes.
   - `updated_map_2.html` highlighting specific nodes in red (e.g., newly added or important nodes).

This script allows visualization and validation of the final street network before use in further analyses or routing applications.

---

## Requirements

- Python 3.8+
- Packages:
  ```bash
  pip install pandas networkx matplotlib folium openpyxl
