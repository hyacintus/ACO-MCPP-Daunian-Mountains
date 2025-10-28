import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import webbrowser

# Carica i nodi filtrati
nodes_df = pd.read_csv('3_nodes_renamed_filtered.csv')

# Carica gli archi filtrati
edges_df = pd.read_csv('3_edges_labeled_filtered.csv')

# Elimina tutti gli archi con label = 1
edges_df = edges_df[edges_df['label'] != 1]

# Rinomina gli ID dei nodi e aggiorna gli ID nei dati degli archi
new_node_ids = list(range(1, len(nodes_df) + 1))
node_id_mapping = dict(zip(nodes_df['ID'], new_node_ids))

nodes_df['ID'] = new_node_ids
edges_df['node u'] = edges_df['node u'].map(node_id_mapping)
edges_df['node v'] = edges_df['node v'].map(node_id_mapping)

# Salva i nodi filtrati e gli archi filtrati nei nuovi file "4"
nodes_df.to_csv('4_nodes.csv', index=False)
edges_df.to_csv('4_edges.csv', index=False)

# CREAZIONE DEL GRAFO
G = nx.MultiDiGraph()

# Aggiungi nodi con posizione
node_positions = {}
for idx, row in nodes_df.iterrows():
    node_positions[row['ID']] = (row['longitudine'], row['latitudine'])
    G.add_node(row['ID'], pos=(row['longitudine'], row['latitudine']))

# Aggiungi archi
for idx, row in edges_df.iterrows():
    G.add_edge(row['node u'], row['node v'])

# Funzione per identificare i doppi archi
def find_duplicate_edges(G):
    duplicates = []
    for u, v in G.edges():
        count_uv = len(G.get_edge_data(u, v)) if G.get_edge_data(u, v) else 0
        count_vu = len(G.get_edge_data(v, u)) if G.get_edge_data(v, u) else 0
        if count_uv > 1 or count_vu > 1:
            duplicates.append((u, v))
    return duplicates

# Trova i doppi archi
duplicate_edges = find_duplicate_edges(G)

# DISEGNO DEL GRAFO
plt.figure(figsize=(10, 8))

# Estrai le posizioni dei nodi
node_pos = nx.get_node_attributes(G, 'pos')

# Disegna i nodi
nx.draw_networkx_nodes(G, node_pos, node_size=500, node_color='skyblue', edgecolors='black')

# Disegna gli archi
for edge in G.edges(data=True):
    u, v = edge[:2]
    color = 'red' if (u, v) in duplicate_edges or (v, u) in duplicate_edges else 'black'
    nx.draw_networkx_edges(G, node_pos, edgelist=[(u, v)], edge_color=color, arrows=True)

# Aggiungi etichette (ID dei nodi)
nx.draw_networkx_labels(G, node_pos, font_size=12, font_color='black')

plt.title('Grafo con doppi archi evidenziati in rosso')
plt.axis('off')
plt.show()

print("Grafo generato correttamente.")

# Creazione della mappa con Folium
m = folium.Map(location=[nodes_df['latitudine'].mean(), nodes_df['longitudine'].mean()], zoom_start=14)

# Aggiungi i nodi alla mappa con icone numerate
for idx, row in nodes_df.iterrows():
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
