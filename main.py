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

# ── Cenário 8: Verificação geométrica básica ──────────────────────────────────

print("\n=== Cenário 8: Verificação geométrica básica ===")

c1 = Circle(center=(0.0, 0.0), radius=2.0, label="C1")

p_dentro = (1.0, 1.0)
p_fora   = (3.0, 3.0)

seg1_p1, seg1_p2 = (-4.0, 0.0), (4.0, 0.0)   # atravessa o círculo
seg2_p1, seg2_p2 = (-4.0, 3.0), (4.0, 3.0)   # não atravessa

print(f"  Ponto {p_dentro} dentro de C1? {c1.contains_point(p_dentro)}")
print(f"  Ponto {p_fora}  dentro de C1? {c1.contains_point(p_fora)}")
print(f"  Segmento {seg1_p1}→{seg1_p2} intercepta C1? {c1.intersects_segment(seg1_p1, seg1_p2)}")
print(f"  Segmento {seg2_p1}→{seg2_p2} intercepta C1? {c1.intersects_segment(seg2_p1, seg2_p2)}")

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("#0e0e14")
ax.set_facecolor("#13131f")

# Círculo
patch = patches.Circle(
    c1.center, c1.radius,
    facecolor=(0.2, 0.6, 0.8, 0.15),
    edgecolor=(0.2, 0.6, 0.8, 1.0), linewidth=2
)
ax.add_patch(patch)
ax.text(c1.cx, c1.cy + c1.radius * 0.1, c1.label,
        color=(0.2, 0.6, 0.8, 1.0), fontsize=10,
        ha="center", fontfamily="monospace")

# Pontos
ax.plot(*p_dentro, "o", color="#00e676", markersize=10, zorder=5)
ax.text(p_dentro[0] + 0.15, p_dentro[1] + 0.15, "dentro",
        color="#00e676", fontsize=9, fontfamily="monospace")

ax.plot(*p_fora, "o", color="#ff1744", markersize=10, zorder=5)
ax.text(p_fora[0] + 0.15, p_fora[1] + 0.15, "fora",
        color="#ff1744", fontsize=9, fontfamily="monospace")

# Segmentos
ax.plot([seg1_p1[0], seg1_p2[0]], [seg1_p1[1], seg1_p2[1]],
        color="#00e676", linewidth=2, label="segmento intercepta")
ax.plot([seg2_p1[0], seg2_p2[0]], [seg2_p1[1], seg2_p2[1]],
        color="#ff1744", linewidth=2, linestyle="--", label="segmento não intercepta")

ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect("equal")
ax.set_title("Cenário 8 — Verificação geométrica básica", color="white", fontsize=13)
ax.set_xlabel("x", color="#aaa")
ax.set_ylabel("y", color="#aaa")
ax.tick_params(colors="#666")
ax.grid(True, color="#222", linewidth=0.5, linestyle="--")
for spine in ax.spines.values():
    spine.set_edgecolor("#333")
plt.tight_layout()
plt.show()