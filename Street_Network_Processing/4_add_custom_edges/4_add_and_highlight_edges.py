import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import webbrowser

# Definizione degli archi da aggiungere                   <---------------------------  CAMBIARE!!!!!
new_edges_list = [(28, 13), (13, 27), (27, 6), (6, 38)]  # []

# Caricamento dei nodi filtrati
nodes_df = pd.read_csv('4_nodes.csv')

# Caricamento degli archi filtrati
edges_df = pd.read_csv('4_edges.csv')


# Funzione per rimuovere archi esistenti e aggiungere nuovi archi
def update_edges(edges_df, new_edges_list):
    updated_edges = edges_df.copy()
    removed_edges = []

    for u, v in new_edges_list:
        # Trova gli archi da rimuovere (sia u -> v che v -> u)
        remove_idx_uv = updated_edges[(updated_edges['node u'] == u) & (updated_edges['node v'] == v)].index
        remove_idx_vu = updated_edges[(updated_edges['node u'] == v) & (updated_edges['node v'] == u)].index

        # Rimuovi l'arco u -> v, se presente
        if not remove_idx_uv.empty:
            removed_edges.append(updated_edges.loc[remove_idx_uv, ['node u', 'node v', 'length']])
            updated_edges = updated_edges.drop(remove_idx_uv)

        # Rimuovi l'arco v -> u, se presente
        if not remove_idx_vu.empty:
            removed_edges.append(updated_edges.loc[remove_idx_vu, ['node u', 'node v', 'length']])
            updated_edges = updated_edges.drop(remove_idx_vu)

        # Aggiungi il nuovo arco u -> v
        new_edge_data = {
            'node u': [u],
            'node v': [v],
            'length': removed_edges[-1]['length'].values[0] if removed_edges else None,
            'label': 1
        }

        # Converti new_edge_data in DataFrame solo se ci sono dati validi da aggiungere
        if new_edge_data['node u'] and new_edge_data['node v']:
            new_edge_df = pd.DataFrame(new_edge_data)
            updated_edges = pd.concat([updated_edges, new_edge_df], ignore_index=True)

    return updated_edges, removed_edges


# Aggiorna gli archi
updated_edges_df, removed_edges_info = update_edges(edges_df, new_edges_list)

# Aggiorna gli ID dei nodi e salva i file "5_nodes.csv" e "5_edges.csv"
updated_nodes_df = nodes_df.copy()
updated_nodes_df.to_csv('5_nodes.csv', index=False)
updated_edges_df.to_csv('5_edges.csv', index=False)

print("File '5_nodes.csv' e '5_edges.csv' creati correttamente.")

# CREAZIONE DEL GRAFO AGGIORNATO
G_updated = nx.MultiDiGraph()

# Aggiungi nodi con posizione
node_positions_updated = {}
for idx, row in updated_nodes_df.iterrows():
    node_positions_updated[row['ID']] = (row['longitudine'], row['latitudine'])
    G_updated.add_node(row['ID'], pos=(row['longitudine'], row['latitudine']))

# Aggiungi archi aggiornati
for idx, row in updated_edges_df.iterrows():
    G_updated.add_edge(row['node u'], row['node v'], label=row['label'])

# DISEGNO DEL GRAFO AGGIORNATO
plt.figure(figsize=(10, 8))

# Estrai le posizioni dei nodi aggiornati
node_pos_updated = nx.get_node_attributes(G_updated, 'pos')

# Disegna i nodi
nx.draw_networkx_nodes(G_updated, node_pos_updated, node_size=500, node_color='skyblue', edgecolors='black')

# Disegna gli archi
for edge in G_updated.edges(data=True):
    u, v, edge_attr = edge
    edge_color = 'red' if edge_attr['label'] == 1 else 'black'
    nx.draw_networkx_edges(G_updated, node_pos_updated, edgelist=[(u, v)], edge_color=edge_color, arrows=True)

# Aggiungi etichette (ID dei nodi)
nx.draw_networkx_labels(G_updated, node_pos_updated, font_size=12, font_color='black')

plt.title('Grafo aggiornato con archi di label 1 colorati di rosso')
plt.axis('off')
plt.show()

print("Grafo aggiornato generato correttamente.")

# Estrazione dei numeri unici
highlight_node_ids = list(set([num for edge in new_edges_list for num in edge]))

# Creazione della mappa con Folium per i nodi aggiornati
m = folium.Map(location=[updated_nodes_df['latitudine'].mean(), updated_nodes_df['longitudine'].mean()], zoom_start=14)

# Aggiungi i nodi alla mappa con icone numerate
for idx, row in updated_nodes_df.iterrows():
    if row['ID'] in highlight_node_ids:
        color = 'red'
    else:
        color = 'blue'

    folium.Marker(
        location=[row['latitudine'], row['longitudine']],
        icon=folium.DivIcon(html=f"""
            <div style="font-family: Arial; color: white; background-color: {color}; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
                {row['ID']}
            </div>"""
                            )
    ).add_to(m)

# Salva la mappa in un file HTML
m.save('updated_map.html')

print(f"Mappa aggiornata generata correttamente: 'updated_map.html'")

# Apre la mappa nel browser predefinito
webbrowser.open('updated_map.html')


