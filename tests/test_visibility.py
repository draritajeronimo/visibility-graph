"""
test_visibility.py
Testes unitários para o sistema de grafos de visibilidade.
"""

import sys
sys.path.insert(0, 'src')

from circle import Circle
from visibility import classify_visibility


# ── Cenário 1: Visibilidade total ─────────────────────────────────────────────

def test_visibilidade_total_sem_obstaculos():
    """Dois círculos sem nenhum obstáculo — deve ser visível (0)."""
    c1 = Circle(center=(0.0, 0.0), radius=1.0)
    c2 = Circle(center=(5.0, 0.0), radius=1.0)
    assert classify_visibility(c1, c2, obstacles=[], n_samples=32) == 0


def test_visibilidade_total_triangulo():
    """Três círculos em triângulo — todos os pares devem ser visíveis (0)."""
    c1 = Circle(center=(0.0, 0.0), radius=1.0)
    c2 = Circle(center=(6.0, 0.0), radius=1.0)
    c3 = Circle(center=(3.0, 5.0), radius=1.0)

    assert classify_visibility(c1, c2, obstacles=[c3], n_samples=32) == 0
    assert classify_visibility(c1, c3, obstacles=[c2], n_samples=32) == 0
    assert classify_visibility(c2, c3, obstacles=[c1], n_samples=32) == 0


# ── Cenário 2: Bloqueio parcial ───────────────────────────────────────────────

def test_bloqueio_parcial():
    """Obstáculo deslocado — deve ser bloqueio parcial (1)."""
    c1 = Circle(center=(0.0, 0.0), radius=1.0)
    c2 = Circle(center=(4.0, 1.5), radius=1.0)  # deslocado
    c3 = Circle(center=(8.0, 0.0), radius=1.0)

    assert classify_visibility(c1, c3, obstacles=[c2], n_samples=64) == 1


# ── Cenário 3: Bloqueio total ─────────────────────────────────────────────────

def test_bloqueio_total():
    """Obstáculo central com raio maior — deve ser bloqueio total (2)."""
    c1 = Circle(center=(0.0, 0.0), radius=1.0)
    c2 = Circle(center=(4.0, 0.0), radius=1.5)  # no meio, raio maior
    c3 = Circle(center=(8.0, 0.0), radius=1.0)

    assert classify_visibility(c1, c3, obstacles=[c2], n_samples=64) == 2


# ── Testes da classe Circle ───────────────────────────────────────────────────

def test_circle_raio_invalido():
    """Raio negativo deve lançar exceção."""
    try:
        Circle(center=(0.0, 0.0), radius=-1.0)
        assert False, "Deveria ter lançado ValueError"
    except ValueError:
        pass


def test_circle_contains_point():
    """Ponto dentro do círculo deve retornar True."""
    c = Circle(center=(0.0, 0.0), radius=2.0)
    assert c.contains_point((0.0, 0.0)) == True
    assert c.contains_point((1.0, 1.0)) == True
    assert c.contains_point((3.0, 0.0)) == False


def test_circle_intersects_segment():
    """Segmento passando pelo centro deve interceptar o círculo."""
    c = Circle(center=(0.0, 0.0), radius=1.0)
    assert c.intersects_segment((-2.0, 0.0), (2.0, 0.0)) == True
    assert c.intersects_segment((2.0, 0.0), (5.0, 0.0)) == False