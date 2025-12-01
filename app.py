import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import time
import os
import networkx as nx
from pyvis.network import Network
# Matplotlib removed due to installation issues on MinGW
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Intentar importar el motor C++
try:
    from neuronet import NeuroNetEngine
    BACKEND_TYPE = "C++ (Optimized)"
except ImportError:
    BACKEND_TYPE = "Python (Fallback)"
    print("Advertencia: No se pudo cargar la extension C++. Usando fallback en Python.")
    
    # Fallback implementation for testing GUI without compilation
    class NeuroNetEngine:
        def __init__(self):
            self.adj = {}
            self.num_aristas = 0
            
        def cargar_datos(self, archivo):
            print(f"[Python Fallback] Cargando {archivo}...")
            self.adj = {}
            self.num_aristas = 0
            with open(archivo, 'r') as f:
                for line in f:
                    if not line.strip() or line.startswith('#'): continue
                    parts = line.split()
                    if len(parts) >= 2:
                        u, v = int(parts[0]), int(parts[1])
                        if u not in self.adj: self.adj[u] = []
                        self.adj[u].append(v)
                        self.num_aristas += 1
            print(f"[Python Fallback] Carga completa. Nodos: {len(self.adj)}")

        def obtener_nodo_mayor_grado(self):
            if not self.adj: return (-1, 0)
            max_node = max(self.adj, key=lambda k: len(self.adj[k]))
            return (max_node, len(self.adj[max_node]))

        def bfs(self, inicio, profundidad_max):
            visitados = []
            if inicio not in self.adj: return visitados
            
            queue = [(inicio, 0)]
            seen = {inicio}
            
            # Para coincidir con la logica C++, retornamos aristas exploradas
            # Pero aqui simplificamos a aristas del arbol BFS
            
            idx = 0
            while idx < len(queue):
                u, dist = queue[idx]
                idx += 1
                
                if dist >= profundidad_max: continue
                
                if u in self.adj:
                    for v in self.adj[u]:
                        visitados.append((u, v))
                        if v not in seen:
                            seen.add(v)
                            queue.append((v, dist + 1))
            return visitados

        def obtener_estadisticas(self):
            return {"nodos": len(self.adj), "aristas": self.num_aristas}

class NeuroNetApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"NeuroNet - Analisis de Redes Masivas [{BACKEND_TYPE}]")
        self.root.geometry("1000x800")
        
        self.engine = NeuroNetEngine()
        self.graph_data = None
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Frame de Controles
        control_frame = ttk.LabelFrame(self.root, text="Panel de Control", padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Carga de Archivo
        ttk.Button(control_frame, text="Cargar Dataset (Edge List)", command=self.load_file).grid(row=0, column=0, padx=5, pady=5)
        self.lbl_file = ttk.Label(control_frame, text="Ningun archivo cargado")
        self.lbl_file.grid(row=0, column=1, padx=5, pady=5)
        
        # Metricas
        self.lbl_stats = ttk.Label(control_frame, text="Nodos: 0 | Aristas: 0 | Memoria: --")
        self.lbl_stats.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Analisis
        ttk.Separator(control_frame, orient='horizontal').grid(row=2, column=0, columnspan=4, sticky='ew', pady=5)
        
        ttk.Button(control_frame, text="Calcular Nodo Critico (Max Grado)", command=self.find_critical_node).grid(row=3, column=0, padx=5, pady=5)
        self.lbl_critical = ttk.Label(control_frame, text="--")
        self.lbl_critical.grid(row=3, column=1, padx=5, pady=5)
        
        # Simulacion BFS
        ttk.Label(control_frame, text="Nodo Inicio:").grid(row=4, column=0, sticky='e')
        self.ent_start_node = ttk.Entry(control_frame, width=10)
        self.ent_start_node.grid(row=4, column=1, sticky='w')
        
        ttk.Label(control_frame, text="Profundidad:").grid(row=4, column=2, sticky='e')
        self.ent_depth = ttk.Entry(control_frame, width=5)
        self.ent_depth.insert(0, "2")
        self.ent_depth.grid(row=4, column=3, sticky='w')
        
        ttk.Button(control_frame, text="Ejecutar Simulacion BFS", command=self.run_bfs).grid(row=4, column=4, padx=5)
        
        # Area de Visualizacion
        self.viz_frame = ttk.LabelFrame(self.root, text="Visualizacion de Subgrafo", padding=10)
        self.viz_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = None

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filename: return
        
        self.lbl_file.config(text=os.path.basename(filename))
        self.root.update()
        
        start_time = time.time()
        self.engine.cargar_datos(filename)
        elapsed = time.time() - start_time
        
        stats = self.engine.obtener_estadisticas()
        self.lbl_stats.config(text=f"Nodos: {stats['nodos']} | Aristas: {stats['aristas']} | Carga: {elapsed:.4f}s")
        messagebox.showinfo("Carga Completa", f"Dataset cargado en {elapsed:.4f} segundos.")

    def find_critical_node(self):
        start_time = time.time()
        node, degree = self.engine.obtener_nodo_mayor_grado()
        elapsed = time.time() - start_time
        
        self.lbl_critical.config(text=f"Nodo {node} (Grado {degree})")
        messagebox.showinfo("Resultado", f"Nodo critico encontrado en {elapsed:.4f}s")

    def run_bfs(self):
        try:
            start_node = int(self.ent_start_node.get())
            depth = int(self.ent_depth.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numericos validos.")
            return
            
        start_time = time.time()
        edges = self.engine.bfs(start_node, depth)
        elapsed = time.time() - start_time
        
        print(f"BFS encontrado {len(edges)} aristas en {elapsed:.4f}s")
        self.visualize_subgraph(edges, start_node)

    def visualize_subgraph(self, edges, start_node):
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
            
        if not edges:
            ttk.Label(self.viz_frame, text="No se encontraron conexiones.").pack()
            return

        # Check removed as we are using PyVis now

        # Crear grafo NetworkX para visualizacion
        G = nx.DiGraph()
        G.add_edges_from(edges)
        
        # Visualizacion interactiva con PyVis
        try:
            net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
            net.from_nx(G)
            
            # Resaltar nodo inicial
            for node in net.nodes:
                if node['id'] == start_node:
                    node['color'] = '#ff4444'
                    node['size'] = 30
                    node['title'] = "Nodo Inicio"
            
            output_file = "graph_viz.html"
            net.save_graph(output_file)
            
            abs_path = os.path.abspath(output_file)
            webbrowser.open(f'file://{abs_path}')
            
            ttk.Label(self.viz_frame, text=f"Visualizacion generada exitosamente.\nSe ha abierto en tu navegador:\n{abs_path}").pack(pady=20)
            
        except Exception as e:
            ttk.Label(self.viz_frame, text=f"Error al generar visualizacion: {str(e)}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetApp(root)
    root.mainloop()
