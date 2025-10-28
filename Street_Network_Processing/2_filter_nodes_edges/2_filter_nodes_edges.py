import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import webbrowser

# Carica i nodi rinominati
nodes_df = pd.read_csv('1_nodes_renamed.csv')

# Carica gli archi etichettati
edges_df = pd.read_csv('2_edges_labeled.csv')

# Lista di nodi da rimuovere (puoi sostituire con la tua lista desiderata)  # <------------------------CAMBIARE !!!!
nodes_to_remove = [28, 29]

# Filtra i nodi e gli archi
nodes_df_filtered = nodes_df[~nodes_df['ID'].isin(nodes_to_remove)]
edges_df_filtered = edges_df[~edges_df['node u'].isin(nodes_to_remove) & ~edges_df['node v'].isin(nodes_to_remove)]

# Salva i nodi filtrati in un nuovo file CSV
nodes_df_filtered.to_csv('3_nodes_renamed_filtered.csv', index=False)

# Salva gli archi filtrati in un nuovo file CSV
edges_df_filtered.to_csv('3_edges_labeled_filtered.csv', index=False)

print("Nodi e archi filtrati salvati correttamente.")

# CREAZIONE DEL GRAFO
G_filtered = nx.MultiDiGraph()

# Aggiungi nodi filtrati con posizione
node_positions_filtered = {}
for idx, row in nodes_df_filtered.iterrows():
    node_positions_filtered[row['ID']] = (row['longitudine'], row['latitudine'])
    G_filtered.add_node(row['ID'], pos=(row['longitudine'], row['latitudine']))

# Aggiungi archi filtrati
for idx, row in edges_df_filtered.iterrows():
    if row['label'] == 1:
        G_filtered.add_edge(row['node u'], row['node v'])
    else:
        G_filtered.add_edge(row['node u'], row['node v'])
        G_filtered.add_edge(row['node v'], row['node u'])

# DISEGNO DEL GRAFO
plt.figure(figsize=(10, 8))

# Estrai le posizioni dei nodi
node_pos_filtered = nx.get_node_attributes(G_filtered, 'pos')

# Disegna i nodi
nx.draw_networkx_nodes(G_filtered, node_pos_filtered, node_size=500, node_color='skyblue', edgecolors='black')

# Disegna gli archi
nx.draw_networkx_edges(G_filtered, node_pos_filtered, arrows=True)

# Aggiungi etichette (ID dei nodi)
nx.draw_networkx_labels(G_filtered, node_pos_filtered, font_size=12, font_color='black')

plt.title('Grafo filtrato con nodi posizionati tramite latitudine e longitudine')
plt.axis('off')
plt.show()

# Creazione della mappa con Folium
m = folium.Map(location=[nodes_df_filtered['latitudine'].mean(), nodes_df_filtered['longitudine'].mean()], zoom_start=14)

# Aggiungi i nodi alla mappa con icone numerate
for idx, row in nodes_df_filtered.iterrows():
    folium.Marker(
        location=[row['latitudine'], row['longitudine']],
        icon=folium.DivIcon(html=f"""
            <div style="font-family: Arial; color: white; background-color: blue; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
                {row['ID']}
            </div>"""
        )
    ).add_to(m)

# Salva la mappa in un file HTML
m.save('filtered_map.html')

print(f"Mappa generata correttamente: 'filtered_map.html'")

# Apre la mappa nel browser predefinito
webbrowser.open('filtered_map.html')
