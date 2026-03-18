"""
main.py
Demonstração do grafo de visibilidade entre círculos no R².

Cenários:
    1) Um círculo
    2) Dois círculos
    3) Três círculos
"""

import sys
sys.path.insert(0, 'src')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from circle import Circle
from graph import build_graph, plot_graph


def plotar_circulos(circles, titulo):
    """Plota uma lista de círculos no plano R²."""
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("#0e0e14")
    ax.set_facecolor("#13131f")

    colors = plt.cm.cool(np.linspace(0.2, 0.85, len(circles)))
    for circle, color in zip(circles, colors):
        patch = patches.Circle(
            circle.center, circle.radius,
            facecolor=(*color[:3], 0.15),
            edgecolor=color, linewidth=2
        )
        ax.add_patch(patch)
        ax.plot(*circle.center, "o", color=color, markersize=5)
        ax.text(circle.cx, circle.cy + circle.radius * 0.1,
                circle.label, color=color, fontsize=10,
                ha="center", fontfamily="monospace")

    ax.autoscale()
    ax.margins(0.4)
    ax.set_aspect("equal")
    ax.set_title(titulo, color="white", fontsize=13)
    ax.set_xlabel("x", color="#aaa")
    ax.set_ylabel("y", color="#aaa")
    ax.tick_params(colors="#666")
    ax.grid(True, color="#222", linewidth=0.5, linestyle="--")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    plt.tight_layout()
    plt.show()


# ── Cenário 1: Um círculo ─────────────────────────────────────────────────────

print("=== Cenário 1: Um círculo ===")

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")

print(c1)
plotar_circulos([c1], "Cenário 1 — Um círculo")


# ── Cenário 2: Dois círculos ──────────────────────────────────────────────────

print("\n=== Cenário 2: Dois círculos ===")

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 0.0), radius=1.0, label="C2")

circles = [c1, c2]
plotar_circulos(circles, "Cenário 2 — Dois círculos")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
for i, j, data in G.edges(data=True):
    w = data["weight"]
    status = ["visível", "parcial", "bloqueado"][w]
    simbolo = ["✅", "⚠️", "❌"][w]
    print(f"  {simbolo} {circles[i].label} — {circles[j].label}: {status}")

plot_graph(circles, G)


# ── Cenário 3: Três círculos ──────────────────────────────────────────────────

print("\n=== Cenário 3: Três círculos ===")

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 1.5), radius=1.0, label="C2")  # obstáculo deslocado
c3 = Circle(center=(8.0, 0.0), radius=1.0, label="C3")

circles = [c1, c2, c3]
plotar_circulos(circles, "Cenário 3 — Três círculos")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
for i, j, data in G.edges(data=True):
    w = data["weight"]
    status = ["visível", "parcial", "bloqueado"][w]
    simbolo = ["✅", "⚠️", "❌"][w]
    print(f"  {simbolo} {circles[i].label} — {circles[j].label}: {status}")

plot_graph(circles, G)

# ── Cenário 6: Três círculos — visibilidade total ─────────────────────────────

print("\n=== Cenário 6: Três círculos — visibilidade total ===")

# Círculos em triângulo: nenhum fica no caminho dos outros
c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(6.0, 0.0), radius=1.0, label="C2")
c3 = Circle(center=(3.0, 5.0), radius=1.0, label="C3")

circles = [c1, c2, c3]
plotar_circulos(circles, "Cenário 6 — Três círculos")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
for i, j, data in G.edges(data=True):
    w = data["weight"]
    status = ["visível", "parcial", "bloqueado"][w]
    simbolo = ["✅", "⚠️", "❌"][w]
    print(f"  {simbolo} {circles[i].label} — {circles[j].label}: {status}")

plot_graph(circles, G)

# ── Cenário 7: Três círculos — bloqueio total ─────────────────────────────────

print("\n=== Cenário 7: Três círculos — bloqueio total ===")

# C2 está exatamente no meio entre C1 e C3, com raio maior para garantir bloqueio total
c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 0.0), radius=1.5, label="C2")  # obstáculo central
c3 = Circle(center=(8.0, 0.0), radius=1.0, label="C3")

circles = [c1, c2, c3]
plotar_circulos(circles, "Cenário 7 — Três círculos")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
for i, j, data in G.edges(data=True):
    w = data["weight"]
    status = ["visível", "parcial", "bloqueado"][w]
    simbolo = ["✅", "⚠️", "❌"][w]
    print(f"  {simbolo} {circles[i].label} — {circles[j].label}: {status}")

plot_graph(circles, G)