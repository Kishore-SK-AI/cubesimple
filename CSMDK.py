import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load file
df = pd.read_excel("Christus_Clinical_CSDM_Mapping_Merged (1).xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Get columns dynamically
cols = df.columns.tolist()

cap_col = cols[0]        # Business Capability
app_col = cols[1]        # Business Application
app_serv_col = cols[2]   # Application Service
serv_col = cols[3]       # Business Service
offer_col = cols[4]      # Business Service Offering

# Remove duplicates
df_cap_app = df[[cap_col, app_col]].drop_duplicates()
df_cap_serv = df[[cap_col, serv_col]].drop_duplicates()
df_app_appserv = df[[app_col, app_serv_col]].drop_duplicates()
df_offer_appserv = df[[offer_col, app_serv_col]].drop_duplicates()
df_offer_serv = df[[offer_col, serv_col]].drop_duplicates()

# Create graph
G = nx.DiGraph()

# 1. Capability → Application (Provided by)
for _, row in df_cap_app.iterrows():
    G.add_edge(row[cap_col], row[app_col], label="Provided by")

# 2. Capability → Business Service (Provided by)
for _, row in df_cap_serv.iterrows():
    G.add_edge(row[cap_col], row[serv_col], label="Provided by")

# 3. Application → Application Service (Consumes)
for _, row in df_app_appserv.iterrows():
    G.add_edge(row[app_col], row[app_serv_col], label="Consumes")

# 4. Offering → Application Service (Depends on)
for _, row in df_offer_appserv.iterrows():
    G.add_edge(row[offer_col], row[app_serv_col], label="Depends on")

# 5. Offering → Business Service (Uses)
for _, row in df_offer_serv.iterrows():
    G.add_edge(row[offer_col], row[serv_col], label="Uses")

# Layout
pos = nx.kamada_kawai_layout(G)

plt.figure(figsize=(18,10))

# Color nodes based on type
colors = []
for node in G.nodes():
    if node in df[cap_col].values:
        colors.append("lightblue")      # Capability
    elif node in df[app_col].values:
        colors.append("lightgreen")     # Application
    elif node in df[app_serv_col].values:
        colors.append("orange")         # App Service
    elif node in df[serv_col].values:
        colors.append("lightcoral")     # Business Service
    else:
        colors.append("violet")         # Service Offering

# Draw nodes & labels
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=3000)
nx.draw_networkx_labels(G, pos, font_size=7)

# Separate edges by relationship type
edges_provided = [(u, v) for u, v, d in G.edges(data=True) if d['label'] == "Provided by"]
edges_consumes = [(u, v) for u, v, d in G.edges(data=True) if d['label'] == "Consumes"]
edges_depends = [(u, v) for u, v, d in G.edges(data=True) if d['label'] == "Depends on"]
edges_uses = [(u, v) for u, v, d in G.edges(data=True) if d['label'] == "Uses"]  # FIXED

# Draw edges with arrows
nx.draw_networkx_edges(
    G, pos,
    edgelist=edges_provided,
    edge_color="blue",
    arrows=True,
    arrowstyle='-|>',
    arrowsize=25,
    width=2,
    connectionstyle='arc3,rad=0.1'
)

nx.draw_networkx_edges(
    G, pos,
    edgelist=edges_consumes,
    edge_color="green",
    arrows=True,
    arrowstyle='-|>',
    arrowsize=25,
    width=2,
    connectionstyle='arc3,rad=0.1'
)

nx.draw_networkx_edges(
    G, pos,
    edgelist=edges_depends,
    edge_color="red",
    arrows=True,
    arrowstyle='-|>',
    arrowsize=25,
    width=2,
    connectionstyle='arc3,rad=0.1'
)

nx.draw_networkx_edges(
    G, pos,
    edgelist=edges_uses,
    edge_color="purple",
    style="dashed",
    arrows=True,
    arrowstyle='-|>',
    arrowsize=25,
    width=2,
    connectionstyle='arc3,rad=0.1'
)

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

# Title
plt.title("Full Relationship Graph (with Directional Arrows)", fontsize=14)

plt.axis('off')
plt.tight_layout()
plt.show()