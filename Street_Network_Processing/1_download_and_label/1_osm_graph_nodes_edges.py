import osmnx as ox
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import webbrowser

# Specifica l'area di interesse
place_name = "Volturino, Italy"   # <----------------------------------------------------------------------- CAMBIARE!!!

# Scarica la rete stradale
G = ox.graph_from_place(place_name, network_type='drive')  # Puoi scegliere il tipo di rete

# Estrai le informazioni dei nodi
nodes = ox.graph_to_gdfs(G, edges=False)

# Crea il DataFrame per i nodi
nodes_df = nodes[['geometry']].reset_index()
nodes_df.columns = ['ID', 'geometry']
nodes_df['latitudine'] = nodes_df['geometry'].apply(lambda x: x.y)
nodes_df['longitudine'] = nodes_df['geometry'].apply(lambda x: x.x)
nodes_df.drop('geometry', axis=1, inplace=True)

# Crea un mapping tra gli ID vecchi e i nuovi ID partendo da 1
nodes_mapping = {old_id: new_id for new_id, old_id in enumerate(nodes_df['ID'], start=1)}

# Aggiungi una nuova colonna con i nuovi ID al DataFrame dei nodi
nodes_df['new_ID'] = nodes_df['ID'].map(nodes_mapping)

# Sostituisci la colonna ID con i nuovi ID
nodes_df['ID'] = nodes_df['new_ID']
nodes_df.drop(columns=['new_ID'], inplace=True)

# Mostra il mapping degli ID vecchi e nuovi
print("Mapping degli ID vecchi e nuovi:")
print(nodes_mapping)

# Salva il DataFrame dei nodi rinominati in un file CSV
nodes_df.to_csv('1_nodes_renamed.csv', index=False)

# Estrai le informazioni degli archi
edges = ox.graph_to_gdfs(G, nodes=False)

# Crea il DataFrame per gli archi
edges_df = edges[['length', 'oneway', 'reversed']].reset_index()
edges_df.drop(columns=[edges_df.columns[2]], inplace=True)  # Elimina la terza colonna
edges_df.columns = ['node u', 'node v', 'length', 'oneway', 'reversed']

# Rinomina gli ID nei dati degli archi usando il mapping creato
edges_df['node u'] = edges_df['node u'].map(nodes_mapping)
edges_df['node v'] = edges_df['node v'].map(nodes_mapping)

# Salva il DataFrame degli archi rinominati in un file CSV
edges_df.to_csv('1_edges_renamed.csv', index=False)

# Converti i valori delle colonne 'oneway' e 'reversed' in booleani
edges_df['oneway'] = edges_df['oneway'].astype(str).map({'True': True, 'False': False})
edges_df['reversed'] = edges_df['reversed'].astype(str).map({'True': True, 'False': False})

# Crea una lista vuota per memorizzare le righe del nuovo DataFrame
new_edges = []

# Itera su ogni riga del DataFrame degli archi
for index, row in edges_df.iterrows():
    node_u = row['node u']
    node_v = row['node v']
    length = row['length']
    oneway = row['oneway']
    reversed = row['reversed']

    if oneway and not reversed:
        label = 1
        new_edges.append([node_u, node_v, length, label])
    elif reversed and not oneway:
        label = 1
        new_edges.append([node_v, node_u, length, label])
    elif not oneway and not reversed:
        label = 0
        new_edges.append([node_u, node_v, length, label])

# Crea un nuovo DataFrame con le colonne specificate
new_edges_df = pd.DataFrame(new_edges, columns=['node u', 'node v', 'length', 'label'])

# Salva il nuovo DataFrame in un file CSV
new_edges_df.to_csv('2_edges_labeled.csv', index=False)

print("Nuovo file CSV con le etichette generato correttamente: '2_edges_labeled.csv'")

# CREAZIONE DEL GRAFO
G = nx.MultiDiGraph()

# Aggiungi nodi con posizione
node_positions = {}
for idx, row in nodes_df.iterrows():
    node_positions[row['ID']] = (row['longitudine'], row['latitudine'])
    G.add_node(row['ID'], pos=(row['longitudine'], row['latitudine']))

# Aggiungi archi
for idx, row in new_edges_df.iterrows():
    if row['label'] == 1:
        G.add_edge(row['node u'], row['node v'])
    else:
        G.add_edge(row['node u'], row['node v'])
        G.add_edge(row['node v'], row['node u'])

# DISEGNO DEL GRAFO
plt.figure(figsize=(10, 8))

# Estrai le posizioni dei nodi
node_pos = nx.get_node_attributes(G, 'pos')

# Disegna i nodi
nx.draw_networkx_nodes(G, node_pos, node_size=500, node_color='skyblue', edgecolors='black')

# Disegna gli archi
nx.draw_networkx_edges(G, node_pos, arrows=True)

# Aggiungi etichette (ID dei nodi)
nx.draw_networkx_labels(G, node_pos, font_size=12, font_color='black')

plt.title('Grafo misto con nodi posizionati tramite latitudine e longitudine')
plt.axis('off')
plt.show()

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
m.save('map.html')

print("Mappa generata correttamente: 'map.html'")
# Apre la mappa nel browser predefinito
webbrowser.open('map.html')
