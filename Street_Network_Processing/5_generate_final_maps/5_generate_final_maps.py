import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import webbrowser

# Caricamento dei nodi e degli archi aggiornati
updated_nodes_df = pd.read_csv('5_nodes.csv')
updated_edges_df = pd.read_csv('5_edges.csv')

# DE COMMENTA QUESTA PARTE OGNI VOLTA
# # CONTROLLO NODI NON COLLEGATI TRA LORO   <------------------------------------------------ ATTENZIONE, POTREBBERO COMPARIRE DEI WARNING!!!
# # Ottieni il massimo della prima colonna (escludendo la prima riga)
# max_value = updated_nodes_df.iloc[1:, 0].max()
#
# # Crea un range di numeri da 1 al massimo della prima colonna (esclusa la prima riga)
# numbers_to_check = set(range(1, max_value + 1))
#
# # Ottieni tutti i numeri presenti nelle prime due colonne di updated_edges_df (escludendo la prima riga)
# edges_numbers = set(updated_edges_df.iloc[1:, 0]).union(set(updated_edges_df.iloc[1:, 1]))
#
# # Controlla quali numeri non sono presenti nelle prime due colonne di 5_edges.csv
# missing_numbers = numbers_to_check - edges_numbers
#
# # Se ci sono numeri mancanti, lancia un'eccezione con il messaggio di warning
# if missing_numbers:
#     # Apre la mappa nel browser predefinito
#     webbrowser.open('updated_map.html')
#
#     # Lista degli ID dei nodi da evidenziare
#     highlight_node_ids = [53]  # Sostituisci con gli ID dei nodi che vuoi evidenziare-----------------------------------------
#
#     # Creazione della mappa con Folium per i nodi aggiornati
#     m_2 = folium.Map(location=[updated_nodes_df['latitudine'].mean(), updated_nodes_df['longitudine'].mean()],
#                      zoom_start=14)
#
#     # Aggiungi i nodi alla mappa con icone numerate, cambiando colore per i nodi evidenziati
#     for idx, row in updated_nodes_df.iterrows():
#         if row['ID'] in highlight_node_ids:
#             color = 'red'
#         else:
#             color = 'blue'
#
#         folium.Marker(
#             location=[row['latitudine'], row['longitudine']],
#             icon=folium.DivIcon(html=f"""
#                 <div style="font-family: Arial; color: white; background-color: {color}; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
#                     {row['ID']}
#                 </div>"""
#                                 )
#         ).add_to(m_2)
#
#     # Salva la mappa in un file HTML
#     m_2.save('updated_map_2.html')
#
#     print(f"Mappa aggiornata generata correttamente: 'updated_map_2.html'")
#
#     # Apre la mappa nel browser predefinito
#     webbrowser.open('updated_map_2.html')
#     raise ValueError(f"Warning: I seguenti numeri sono presenti in 5_nodes.csv ma non in 5_edges.csv: {sorted(missing_numbers)}")
# else:
#     print("Tutti i numeri sono presenti in edges.")

# Identificazione delle righe con label = 0 e aggiunta delle righe invertite
edges_label_0 = updated_edges_df[updated_edges_df['label'] == 0]
edges_label_0_inverted = edges_label_0.rename(columns={'node u': 'node v', 'node v': 'node u'})
updated_edges_df = pd.concat([updated_edges_df, edges_label_0_inverted], ignore_index=True)

# Salva in formato Excel
updated_nodes_df.to_excel('6_nodes.xlsx', index=False, engine='openpyxl')
updated_edges_df.to_excel('6_edges.xlsx', index=False, engine='openpyxl')

# Step 2: Riapri il file Excel e salvalo nuovamente in CSV
# Riapri il file Excel appena salvato
updated_nodes_df_excel = pd.read_excel('6_nodes.xlsx', engine='openpyxl')
updated_edges_df_excel = pd.read_excel('6_edges.xlsx', engine='openpyxl')

# Salva nuovamente come CSV
updated_nodes_df_excel.to_csv('6_nodes.csv', index=False)  # <----------  Non funziona, alla fine fai il copia-incolla del file excel nel csv
updated_edges_df_excel.to_csv('6_edges.csv', index=False)

print("File '6_nodes.csv' e '6_edges.csv' creati correttamente.")

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
for u, v, edge_attr in G_updated.edges(data=True):
    edge_color = 'red' if edge_attr['label'] == 1 else 'black'
    nx.draw_networkx_edges(G_updated, node_pos_updated, edgelist=[(u, v)], edge_color=edge_color, arrows=True)

# Aggiungi etichette (ID dei nodi)
nx.draw_networkx_labels(G_updated, node_pos_updated, font_size=12, font_color='black')

plt.title('Grafo aggiornato con archi di label 1 colorati di rosso')
plt.axis('off')
plt.show()

print("Grafo aggiornato generato correttamente.")

# Creazione della mappa con Folium per i nodi aggiornati
m = folium.Map(location=[updated_nodes_df['latitudine'].mean(), updated_nodes_df['longitudine'].mean()], zoom_start=14)

# Aggiungi i nodi alla mappa con icone numerate
for idx, row in updated_nodes_df.iterrows():
    folium.Marker(
        location=[row['latitudine'], row['longitudine']],
        icon=folium.DivIcon(html=f"""
            <div style="font-family: Arial; color: white; background-color: blue; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
                {row['ID']}
            </div>"""
                            )
    ).add_to(m)

# Salva la mappa in un file HTML
m.save('updated_map.html')

print(f"Mappa aggiornata generata correttamente: 'updated_map.html'")

# Apre la mappa nel browser predefinito
webbrowser.open('updated_map.html')

# Lista degli ID dei nodi da evidenziare   (28, 13), (13, 27), (27, 6), (6, 38)
highlight_node_ids = [50, 28, 13, 27, 6, 38]  # Sostituisci con gli ID dei nodi che vuoi evidenziare-----------------------------------------

# Creazione della mappa con Folium per i nodi aggiornati
m_2 = folium.Map(location=[updated_nodes_df['latitudine'].mean(), updated_nodes_df['longitudine'].mean()], zoom_start=14)

# Aggiungi i nodi alla mappa con icone numerate, cambiando colore per i nodi evidenziati
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
    ).add_to(m_2)

# Salva la mappa in un file HTML
m_2.save('updated_map_2.html')

print(f"Mappa aggiornata generata correttamente: 'updated_map_2.html'")

# Apre la mappa nel browser predefinito
webbrowser.open('updated_map_2.html')

