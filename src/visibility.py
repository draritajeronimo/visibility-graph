"""
visibility.py
Classificação de visibilidade entre dois círculos no R².

Valores retornados:
    0 — visibilidade total  (todos os raios passam livres)
    1 — bloqueio parcial    (alguns raios passam, outros são bloqueados)
    2 — bloqueio total      (nenhum raio chega ao destino)
"""

import numpy as np
from typing import List
from circle import Circle
from ray import ray_is_blocked


def classify_visibility(
    circle_a: Circle,
    circle_b: Circle,
    obstacles: List[Circle],
    n_samples: int = 32,
) -> int:
    """
    Classifica a visibilidade entre circle_a e circle_b.

    Amostra n_samples pontos na fronteira de cada círculo e lança
    raios entre todos os pares. Conta quantos passam livres.

    Args:
        circle_a  : círculo de origem
        circle_b  : círculo de destino
        obstacles : outros círculos que podem bloquear (não inclui a e b)
        n_samples : número de pontos amostrados em cada fronteira

    Returns:
        0 — visibilidade total
        1 — bloqueio parcial
        2 — bloqueio total
    """
    points_a = circle_a.sample_boundary(n_samples)
    points_b = circle_b.sample_boundary(n_samples)

    total = 0
    blocked = 0

    for pa in points_a:
        for pb in points_b:
            total += 1
            if ray_is_blocked(tuple(pa), tuple(pb), obstacles):
                blocked += 1

    if blocked == 0:
        return 0  # visibilidade total
    elif blocked == total:
        return 2  # bloqueio total
    else:
        return 1  # bloqueio parcial