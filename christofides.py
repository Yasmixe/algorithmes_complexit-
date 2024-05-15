import tkinter as tk
from tkinter import scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import math
import matplotlib.pyplot as plt

def generate_result(n):
    result = ""
    # Construction du graphe complet
    G = nx.complete_graph(n)
    my_pos = {i: (random.random(), random.random()) for i in G.nodes}

    # Calcul des distances euclidiennes et ajout des attributs 'length' aux arêtes
    for i, j in G.edges:
        (x1, y1) = my_pos[i]
        (x2, y2) = my_pos[j]
        G.edges[i, j]['length'] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Construction de l'arbre de poids minimum avec l'algorithme de Kruskal
    T = nx.minimum_spanning_tree(G, weight='length')
    result += f"Nombre d'arêtes dans l'arbre de poids minimum (étape 1) : {len(T.edges)}\n"

    # Sélection des nœuds de degré impair et recherche d'un couplage parfait de coût minimum
    odd_degree_nodes = [i for i in T.nodes if T.degree(i) % 2 != 0]
    G_odd = G.subgraph(odd_degree_nodes)
    matching = nx.max_weight_matching(G_odd, weight='length')
    result += f"Couplage parfait de coût minimum (étape 2) : {matching}\n"

    # Construction du multigraphe avec l'union de l'arbre de poids minimum et du couplage parfait
    M = nx.MultiGraph()
    M.add_edges_from(T.edges(data=True))
    M.add_edges_from(matching, weight='length')

    # Calcul du circuit eulérien
    eulerian_circuit = list(nx.eulerian_circuit(M, source=0))

    # Optimisation du parcours eulérien
    optimized_tour = [eulerian_circuit[0][0]]
    for (i, j) in eulerian_circuit:
        if j not in optimized_tour:
            optimized_tour.append(j)
    optimized_tour.append(optimized_tour[0])

    result += f"Tour optimal après optimisation (étape 3) : {optimized_tour}"

    # Affichage du graphe avec le tour optimal
    fig, ax = plt.subplots()
    nx.draw(G.subgraph(optimized_tour), pos=my_pos, with_labels=True, ax=ax)
    ax.set_title("Graphe avec le tour optimal")

    return result, fig

def show_result(n):
    result, fig = generate_result(n)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, result)

    # Afficher la figure dans l'interface tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_submit():
    try:
        num_vertices = int(entry.get())
        show_result(num_vertices)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of vertices.")

root = tk.Tk()
root.title("Christofides Algorithm")

label = tk.Label(root, text="Enter the number of vertices:")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

text_area = scrolledtext.ScrolledText(root, width=80, height=10)
text_area.pack()

root.mainloop()
