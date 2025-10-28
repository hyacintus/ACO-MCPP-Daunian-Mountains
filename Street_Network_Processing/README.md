# Street Network Processing Project

## Overview
This project provides a complete workflow for extracting, processing, and visualizing the street network of a municipality using OpenStreetMap data. The pipeline is modular, with each step handled by a dedicated script and documented with its own README. 

The final goal is to obtain:
- Cleaned and relabeled nodes and edges.
- Labeled edges for directional information.
- Filtered networks according to custom rules.
- Updated graphs with new edges added if necessary.
- Interactive maps for visual inspection and analysis.

---

## Project Structure

### 01_download_and_label
- **Purpose:** Download the street network from OpenStreetMap, extract nodes and edges, relabel node IDs, and label edges as directed or undirected.
- **Main script:** `1_osm_graph_nodes_edges.py`
- **Outputs:** `1_nodes_renamed.csv`, `2_edges_labeled.csv`
- **Readme:** Contains usage instructions and description of the workflow.

### 02_filter_nodes_edges
- **Purpose:** Remove specified nodes and edges from the network to filter out unwanted elements.
- **Main script:** `2_filter_nodes_edges.py`
- **Outputs:** `3_nodes_renamed_filtered.csv`, `3_edges_labeled_filtered.csv`

### 03_remove_oneway_edges
- **Purpose:** Remove edges with `label = 1` (one-way) and update node IDs sequentially.
- **Main script:** `3_relabel_and_highlight_duplicates.py`
- **Outputs:** `4_nodes.csv`, `4_edges.csv`

### 04_add_custom_edges
- **Purpose:** Add or replace custom edges in the network based on project-specific requirements.
- **Main script:** `4_add_and_highlight_edges.py`
- **Outputs:** `5_nodes.csv`, `5_edges.csv`
- **Notes:** Newly added edges are highlighted in red in the interactive maps.

### 05_generate_final_maps
- **Purpose:** Finalize the network for visualization, create bidirectional edges for `label = 0`, save Excel and CSV files, and generate interactive maps for all nodes and highlighted nodes.
- **Main script:** `5_generate_final_maps.py`
- **Outputs:** `6_nodes.xlsx`, `6_edges.xlsx`, `6_nodes.csv`, `6_edges.csv`, `updated_map.html`, `updated_map_2.html`

---

## Requirements
- Python 3.8+
- Packages:
```bash
pip install pandas networkx matplotlib folium osmnx openpyxl
