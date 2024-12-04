# ACO-MCPP-Daunian-Mountains

# Project Overview
This repository contains data used for the analysis presented in the article:
"An analysis of Mixed Chinese Postman Problem by using Ant Colony Optimization on Open Real World Data."

The dataset is organized into a main folder named Data, which includes subfolders corresponding to each municipality of the Subappennino Dauno analyzed in the study. Each subfolder is named after a specific municipality and contains the following three .csv files:
1. Edges.csv
2. Nodes.csv
3. Solution.csv


# File Descriptions
# 1. Edges.csv
This file contains the data required to construct the mixed graphs for the municipalities. The data is structured in four columns as follows:

Column	| Description

Start Node	| ID of the starting node

End Node	| ID of the ending node

Length (m)	| Length of the edge/arc in meters

Label	| 0 for undirected edges, 1 for directed arcs

# 2. Nodes.csv
This file provides the geographical data to represent the nodes on OpenStreetMap. The data is structured in three columns as follows:

Column	| Description

Node | ID	Unique identifier for the node

Latitude	| Latitude coordinate of the node

Longitude	| Longitude coordinate of the node

# 3. Solution.csv
This file represents the augmented graph for one of the possible solutions to the Mixed Chinese Postman Problem (MCPP). The structure of the file is similar to Edges.csv, with the following characteristics:

Column	| Description
Start Node	| ID of the starting node
End Node	| ID of the ending node
Length (m)	| Length of the directed arc in meters
Label	| All entries are 1, as all edges are directed arcs in this Eulerian graph

In this file, some arcs may appear multiple times, reflecting the structure of an Eulerian directed graph. Using Hierholzer's algorithm, one can extract an Eulerian circuit, representing a valid solution to the MCPP.


# Usage
1. Navigate to the Data folder to find subfolders corresponding to each municipality.
2. Use the Edges.csv and Nodes.csv files to visualize and construct mixed graphs for analysis.
3. Use the Solution.csv file to analyze the Eulerian graph and apply Hierholzer’s algorithm to extract an Eulerian circuit.

For more details about the methodology and results, please refer to the original article.
