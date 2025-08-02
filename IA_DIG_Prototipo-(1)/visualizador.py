
import matplotlib.pyplot as plt
import networkx as nx

def mostrar_valor(grafo, key, titulo, cmap=plt.cm.viridis):
    pos = nx.spring_layout(grafo, seed=42)
    valores = [grafo.nodes[n].get(key, 0.0) for n in grafo.nodes]
    etiquetas = {n: f"{n}\n{key[:1]}={grafo.nodes[n].get(key):.2f}" for n in grafo.nodes}
    nx.draw(grafo, pos, with_labels=False, node_color=valores, cmap=cmap, node_size=1200)
    nx.draw_networkx_labels(grafo, pos, labels=etiquetas, font_color='white')
    plt.title(titulo)
    sm = plt.cm.ScalarMappable(cmap=cmap)
    plt.colorbar(sm, label=key)
    plt.axis("off")
    plt.show()

def mostrar_colapso(grafo):
    pos = nx.spring_layout(grafo, seed=42)
    color_map = ['green' if grafo.nodes[n].get("colapsado") else 'gray' for n in grafo.nodes]
    etiquetas = {n: f"{n}\n★" if grafo.nodes[n].get("colapsado") else n for n in grafo.nodes}
    nx.draw(grafo, pos, with_labels=False, node_color=color_map, node_size=1200)
    nx.draw_networkx_labels(grafo, pos, labels=etiquetas, font_color='white')
    plt.title("Colapso Informacional – Núcleo Estable")
    plt.axis("off")
    plt.show()
