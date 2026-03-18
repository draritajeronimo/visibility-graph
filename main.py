"""
main.py
Demonstração do grafo de visibilidade entre círculos no R².

Cenários:
    1) Um círculo
    2) Dois círculos — visibilidade total
    3) Três círculos — bloqueio parcial
    4) Três círculos — visibilidade total
    5) Três círculos — bloqueio total
    6) Verificação geométrica básica
"""

import sys
sys.path.insert(0, 'src')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from circle import Circle
from ray import ray_is_blocked
from graph import build_graph, plot_graph


# ──────────────────────────────────────────────────────────────────────────────
# Funções auxiliares de visualização
# ──────────────────────────────────────────────────────────────────────────────

COLORS = {
    "background_fig" : "#0e0e14",
    "background_ax"  : "#13131f",
    "grid"           : "#222222",
    "spine"          : "#333333",
    "tick"           : "#666666",
    "axis_label"     : "#aaaaaa",
    "livre"          : "#00e676",
    "bloqueado"      : "#ff1744",
    "parcial"        : "#ffd600",
    "centro"         : "#ffffff",
    "raio"           : "#ffffff",
    "intersecao"     : "#ff9100",
}


def estilo_ax(ax, titulo):
    """Aplica estilo escuro padrão ao eixo."""
    ax.set_aspect("equal")
    ax.set_title(titulo, color="white", fontsize=13, pad=12)
    ax.set_xlabel("x", color=COLORS["axis_label"])
    ax.set_ylabel("y", color=COLORS["axis_label"])
    ax.tick_params(colors=COLORS["tick"])
    ax.grid(True, color=COLORS["grid"], linewidth=0.5, linestyle="--")
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["spine"])


def nova_figura(figsize=(7, 7)):
    """Cria figura e eixo com fundo escuro."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(COLORS["background_fig"])
    ax.set_facecolor(COLORS["background_ax"])
    return fig, ax


def desenhar_circulo(ax, circle, color, mostrar_centro=True,
                     mostrar_raio=True, mostrar_samples=False):
    """Desenha um círculo com centro, raio e amostras opcionais."""
    # Área preenchida
    patch = patches.Circle(
        circle.center, circle.radius,
        facecolor=(*color[:3], 0.15),
        edgecolor=color, linewidth=2
    )
    ax.add_patch(patch)

    # Rótulo
    ax.text(circle.cx, circle.cy + circle.radius * 0.12,
            circle.label, color=color, fontsize=10,
            ha="center", fontfamily="monospace", fontweight="bold")

    # Centro
    if mostrar_centro:
        ax.plot(*circle.center, "o", color=COLORS["centro"],
                markersize=5, zorder=6)
        ax.text(circle.cx + 0.1, circle.cy - 0.2, f"({circle.cx:.0f},{circle.cy:.0f})",
                color=COLORS["centro"], fontsize=7, fontfamily="monospace", alpha=0.7)

    # Raio
    if mostrar_raio:
        angulo = np.pi / 4
        px, py = circle.point_at(angulo)
        ax.annotate("", xy=(px, py), xytext=circle.center,
                    arrowprops=dict(arrowstyle="-", color=COLORS["raio"],
                                    linestyle="--", lw=1, alpha=0.5))
        mx, my = (circle.cx + px) / 2, (circle.cy + py) / 2
        ax.text(mx + 0.1, my + 0.1, f"r={circle.radius:.1f}",
                color=COLORS["raio"], fontsize=7,
                fontfamily="monospace", alpha=0.7)

    # Pontos amostrados na fronteira
    if mostrar_samples:
        pts = circle.sample_boundary(32)
        ax.scatter(pts[:, 0], pts[:, 1], color=color,
                   s=8, alpha=0.5, zorder=5)


def plotar_circulos(circles, titulo, mostrar_centro=True,
                    mostrar_raio=True, mostrar_samples=False):
    """Plota uma lista de círculos no plano R²."""
    fig, ax = nova_figura()
    colors = plt.cm.cool(np.linspace(0.2, 0.85, len(circles)))

    for circle, color in zip(circles, colors):
        desenhar_circulo(ax, circle, color,
                         mostrar_centro=mostrar_centro,
                         mostrar_raio=mostrar_raio,
                         mostrar_samples=mostrar_samples)

    ax.autoscale()
    ax.margins(0.4)
    estilo_ax(ax, titulo)
    plt.tight_layout()
    plt.show()


def plotar_raios(circles, idx_origem, idx_destino, titulo, n=16):
    """Plota os raios entre dois círculos mostrando bloqueios."""
    fig, ax = nova_figura(figsize=(9, 6))
    colors = plt.cm.cool(np.linspace(0.2, 0.85, len(circles)))

    c_orig = circles[idx_origem]
    c_dest = circles[idx_destino]
    obstacles = [c for k, c in enumerate(circles)
                 if k != idx_origem and k != idx_destino]

    pts_orig = c_orig.sample_boundary(n)
    pts_dest = c_dest.sample_boundary(n)

    livres = bloqueados = 0
    for pa in pts_orig:
        for pb in pts_dest:
            blocked = ray_is_blocked(tuple(pa), tuple(pb), obstacles)
            color = COLORS["bloqueado"] if blocked else COLORS["livre"]
            alpha = 0.35 if blocked else 0.5
            ax.plot([pa[0], pb[0]], [pa[1], pb[1]],
                    color=color, linewidth=0.7, alpha=alpha)
            if blocked:
                bloqueados += 1
            else:
                livres += 1

    for circle, color in zip(circles, colors):
        desenhar_circulo(ax, circle, color, mostrar_raio=False)

    total = livres + bloqueados
    ax.plot([], [], color=COLORS["livre"],
            label=f"raio livre ({livres}/{total})")
    ax.plot([], [], color=COLORS["bloqueado"],
            label=f"raio bloqueado ({bloqueados}/{total})")
    ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9)

    ax.autoscale()
    ax.margins(0.3)
    estilo_ax(ax, titulo)
    plt.tight_layout()
    plt.show()


def resumo_grafo(circles, G):
    """Imprime o resumo das arestas do grafo."""
    print(f"  Nós: {G.number_of_nodes()}  |  Arestas: {G.number_of_edges()}")
    for i, j, data in G.edges(data=True):
        w = data["weight"]
        status = ["visível", "parcial", "bloqueado"][w]
        simbolo = ["✅", "⚠️", "❌"][w]
        print(f"  {simbolo} {circles[i].label} — {circles[j].label}: {w} ({status})")


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 1: Um círculo
# ──────────────────────────────────────────────────────────────────────────────

print("=" * 50)
print("Cenário 1: Um círculo")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=2.0, label="C1")
print(c1)
print(f"  Área      : {c1.area:.4f}")
print(f"  Perímetro : {c1.perimeter:.4f}")

plotar_circulos([c1], "Cenário 1 — Um círculo",
                mostrar_centro=True, mostrar_raio=True, mostrar_samples=True)


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 2: Dois círculos — visibilidade total
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("Cenário 2: Dois círculos — visibilidade total")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(5.0, 0.0), radius=1.0, label="C2")
circles = [c1, c2]

plotar_circulos(circles, "Cenário 2 — Dois círculos")
plotar_raios(circles, 0, 1, "Cenário 2 — Raios entre C1 e C2")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
resumo_grafo(circles, G)
plot_graph(circles, G)


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 3: Três círculos — bloqueio parcial
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("Cenário 3: Três círculos — bloqueio parcial")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 1.5), radius=1.0, label="C2")
c3 = Circle(center=(8.0, 0.0), radius=1.0, label="C3")
circles = [c1, c2, c3]

plotar_circulos(circles, "Cenário 3 — Três círculos (bloqueio parcial)")
plotar_raios(circles, 0, 2, "Cenário 3 — Raios entre C1 e C3 (C2 como obstáculo)")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
resumo_grafo(circles, G)
plot_graph(circles, G)


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 4: Três círculos — visibilidade total
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("Cenário 4: Três círculos — visibilidade total")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(6.0, 0.0), radius=1.0, label="C2")
c3 = Circle(center=(3.0, 5.0), radius=1.0, label="C3")
circles = [c1, c2, c3]

plotar_circulos(circles, "Cenário 4 — Três círculos (visibilidade total)")
plotar_raios(circles, 0, 1, "Cenário 4 — Raios entre C1 e C2")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
resumo_grafo(circles, G)
plot_graph(circles, G)


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 5: Três círculos — bloqueio total
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("Cenário 5: Três círculos — bloqueio total")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 0.0), radius=1.5, label="C2")
c3 = Circle(center=(8.0, 0.0), radius=1.0, label="C3")
circles = [c1, c2, c3]

plotar_circulos(circles, "Cenário 5 — Três círculos (bloqueio total)")
plotar_raios(circles, 0, 2, "Cenário 5 — Raios entre C1 e C3 (C2 como obstáculo)")

G = build_graph(circles, n_samples=64)
print("\nArestas:")
resumo_grafo(circles, G)
plot_graph(circles, G)


# ──────────────────────────────────────────────────────────────────────────────
# Cenário 6: Verificação geométrica básica
# ──────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 50)
print("Cenário 6: Verificação geométrica básica")
print("=" * 50)

c1 = Circle(center=(0.0, 0.0), radius=2.0, label="C1")

p_dentro = (1.0, 1.0)
p_fora   = (3.0, 3.0)
seg1_p1, seg1_p2 = (-4.0, 0.0), (4.0, 0.0)
seg2_p1, seg2_p2 = (-4.0, 3.0), (4.0, 3.0)

print(f"  Ponto {p_dentro} dentro de C1?              {c1.contains_point(p_dentro)}")
print(f"  Ponto {p_fora} dentro de C1?              {c1.contains_point(p_fora)}")
print(f"  Segmento {seg1_p1}→{seg1_p2} intercepta? {c1.intersects_segment(seg1_p1, seg1_p2)}")
print(f"  Segmento {seg2_p1}→{seg2_p2} intercepta? {c1.intersects_segment(seg2_p1, seg2_p2)}")

fig, ax = nova_figura()

# Círculo com amostras
desenhar_circulo(ax, c1, np.array([0.2, 0.6, 0.8, 1.0]),
                 mostrar_centro=True, mostrar_raio=True, mostrar_samples=True)

# Pontos dentro/fora
ax.plot(*p_dentro, "o", color=COLORS["livre"], markersize=12, zorder=6)
ax.text(p_dentro[0] + 0.2, p_dentro[1] + 0.2, "dentro",
        color=COLORS["livre"], fontsize=9, fontfamily="monospace")

ax.plot(*p_fora, "o", color=COLORS["bloqueado"], markersize=12, zorder=6)
ax.text(p_fora[0] + 0.2, p_fora[1] + 0.2, "fora",
        color=COLORS["bloqueado"], fontsize=9, fontfamily="monospace")

# Segmentos
ax.plot([seg1_p1[0], seg1_p2[0]], [seg1_p1[1], seg1_p2[1]],
        color=COLORS["bloqueado"], linewidth=2.5,
        label="segmento intercepta (bloqueado)", zorder=3)
ax.plot([seg2_p1[0], seg2_p2[0]], [seg2_p1[1], seg2_p2[1]],
        color=COLORS["livre"], linewidth=2.5, linestyle="--",
        label="segmento não intercepta (livre)", zorder=3)

# Pontos de interseção do segmento 1 com o círculo
for t_val in np.linspace(0, 2 * np.pi, 1000):
    px, py = c1.point_at(t_val)
    if abs(py) < 0.05:
        ax.plot(px, py, "o", color=COLORS["intersecao"],
                markersize=10, zorder=7)
ax.plot([], [], "o", color=COLORS["intersecao"],
        markersize=8, label="ponto de interseção")

ax.legend(facecolor="#1e1e2e", labelcolor="white", fontsize=9)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
estilo_ax(ax, "Cenário 6 — Verificação geométrica básica")
plt.tight_layout()
plt.show()

input("\nPressione Enter para encerrar...")