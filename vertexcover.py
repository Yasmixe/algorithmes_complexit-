import tkinter as tk
from tkinter import messagebox

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def vertex_cover(self):
        visited = [False] * self.V

        # Trouver un couplage maximal
        cover = []
        for u in range(self.V):
            if not visited[u]:
                for v in self.adj[u]:
                    if not visited[v]:
                        cover.append(u)
                        cover.append(v)
                        visited[u] = True
                        visited[v] = True
                        break

        return [(cover[i], cover[i+1]) for i in range(0, len(cover), 2)]


def calculate_vertex_cover():
    num_vertices = int(entry_vertices.get())
    G = Graph(num_vertices)

    edges = entry_edges.get("1.0", tk.END).strip().split("\n")
    for edge in edges:
        u, v = map(int, edge.split())
        G.add_edge(u, v)

    cover = G.vertex_cover()
    messagebox.showinfo("Résultat", f"Vertex Cover (approximation 2): {cover}")


# Interface graphique
root = tk.Tk()
root.title("Vertex Cover Approximation")

label_vertices = tk.Label(root, text="Veuillez entrer le nombre de sommets que vous voulez avoir : ")
label_vertices.pack()

entry_vertices = tk.Entry(root)
entry_vertices.pack()

label_edges = tk.Label(root, text="Donnez les aretes correspondants, dans chaque ligne preciser les deux sommets avec un retour a la ligne pour ajouter une nouvelle arete : ")
label_edges.pack()

entry_edges = tk.Text(root, height=5, width=30)
entry_edges.pack()

button_calculate = tk.Button(root, text="Calculer Vertex Cover", command=calculate_vertex_cover)
button_calculate.pack()

root.mainloop()
