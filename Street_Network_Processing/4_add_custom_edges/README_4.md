# Add and Highlight New Edges in Street Network

## Description
This Python script updates a filtered street network by:

1. Adding new edges specified by the user.
2. Removing existing edges between the same nodes if present.
3. Updating the edge list while preserving node positions.
4. Creating a NetworkX graph with updated edges.
5. Highlighting the newly added edges in red in the graph visualization.
6. Generating an interactive Folium map where the updated edges are visually highlighted by coloring their nodes red.

The script allows direct modification of the network based on field observations or planned changes.

---

## Requirements

- Python 3.8+
- Packages:
  ```bash
  pip install pandas networkx matplotlib folium
