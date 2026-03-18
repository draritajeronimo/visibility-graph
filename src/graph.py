"""
graph.py
Construção e visualização do grafo de visibilidade entre círculos no R².

Pesos das arestas:
    0 — visibilidade total
    1 — bloqueio parcial
    2 — bloqueio total
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from typing import List
from circle import Circle
from visibility import classify_visibility


def build_graph(circles: List[Circle], n_samples: int = 32) -> nx.Graph:
    """
    Constrói o grafo completo de visibilidade entre os círculos.

    Para cada par (i, j), classifica a visibilidade usando todos os
    outros círculos como obstáculos.

    Args:
        circles   : lista de círculos (nós do grafo)
        n_samples : pontos amostrados na fronteira de cada círculo

    Returns:
        Grafo networkx com arestas pesadas por 0, 1 ou 2.
    """
    G = nx.Graph()

    # Adiciona os nós
    for i, c in enumerate(circles):
        G.add_node(i, label=c.label, circle=c)

    # Adiciona as arestas para todo par (i, j)
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            # Obstáculos: todos exceto os dois sendo avaliados
            obstacles = [c for k, c in enumerate(circles) if k != i and k != j]

            weight = classify_visibility(
                circles[i], circles[j], obstacles, n_samples
            )
            G.add_edge(i, j, weight=weight)

    return G


def plot_graph(circles: List[Circle], G: nx.Graph) -> None:
    """
    Visualiza os círculos e as arestas do grafo coloridas por peso.

    Cores das arestas:
        Verde   (#00e676) — peso 0: visibilidade total
        Amarelo (#ffd600) — peso 1: bloqueio parcial
        Vermelho (#ff1744) — peso 2: bloqueio total
    """
    fig, ax = plt.subplots(figsize=(9, 9))
    fig.patch.set_facecolor("#0e0e14")
    ax.set_facecolor("#13131f")

    edge_colors = {0: "#00e676", 1: "#ffd600", 2: "#ff1744"}
    edge_labels = {0: "visível", 1: "parcial", 2: "bloqueado"}

    # Desenha as arestas — peso maior fica por cima (zorder)
    for i, j, data in G.edges(data=True):
        w = data["weight"]
        ci, cj = circles[i], circles[j]
        color = edge_colors[w]

        ax.plot(
            [ci.cx, cj.cx], [ci.cy, cj.cy],
            color=color, linewidth=1.5, alpha=0.8, zorder=w + 1,
        )

        # Número do peso em cada aresta — deslocado perpendicularmente
        mx, my = (ci.cx + cj.cx) / 2, (ci.cy + cj.cy) / 2

        dx, dy = cj.cx - ci.cx, cj.cy - ci.cy
        length = np.sqrt(dx ** 2 + dy ** 2) or 1.0
        px, py = -dy / length, dx / length
        offset = 0.5
        lx, ly = mx + px * offset, my + py * offset

        ax.text(lx, ly, str(w), color=color,
                fontsize=10, ha="center", va="center",
                fontfamily="monospace", fontweight="bold",
                bbox=dict(facecolor="#0e0e14", edgecolor=color,
                          boxstyle="round,pad=0.3", linewidth=1),
                zorder=w + 2)

    # Desenha os círculos
    colors = plt.cm.cool(np.linspace(0.2, 0.85, len(circles)))
    for circle, color in zip(circles, colors):
        filled = patches.Circle(
            circle.center, circle.radius,
            facecolor=(*color[:3], 0.15),
            edgecolor=color, linewidth=2,
            zorder=5,
        )
        ax.add_patch(filled)
        ax.plot(*circle.center, "o", color=color, markersize=5, zorder=6)
        ax.text(
            circle.cx, circle.cy + circle.radius * 0.08,
            circle.label, color=color, fontsize=9,
            ha="center", fontfamily="monospace", zorder=6,
        )

    # Legenda manual
    for w, color in edge_colors.items():
        ax.plot([], [], color=color, linewidth=2, label=f"{w} — {edge_labels[w]}")
    ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9, loc="upper right")

    # Ajuste de limites
    all_bb = [c.bounding_box for c in circles]
    x_min = min(b[0] for b in all_bb)
    y_min = min(b[1] for b in all_bb)
    x_max = max(b[2] for b in all_bb)
    y_max = max(b[3] for b in all_bb)
    margin = max((x_max - x_min), (y_max - y_min)) * 0.25 + 1.0
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)

    ax.set_aspect("equal")
    ax.set_title("Grafo de Visibilidade entre Círculos no R²",
                 color="white", fontsize=13, pad=12)
    ax.set_xlabel("x", color="#aaa")
    ax.set_ylabel("y", color="#aaa")
    ax.tick_params(colors="#666")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.grid(True, color="#222", linewidth=0.5, linestyle="--")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
    c2 = Circle(center=(3.0, 0.0), radius=1.0, label="C2")
    c3 = Circle(center=(6.0, 0.0), radius=1.0, label="C3")
    c4 = Circle(center=(3.0, 5.0), radius=1.0, label="C4")

    circles = [c1, c2, c3, c4]

    print("Construindo grafo de visibilidade...")
    G = build_graph(circles, n_samples=32)

    print("\nArestas e pesos:")
    for i, j, data in G.edges(data=True):
        w = data["weight"]
        status = ["visível", "parcial", "bloqueado"][w]
        print(f"  {circles[i].label} — {circles[j].label}: {w} ({status})")

    plot_graph(circles, G)