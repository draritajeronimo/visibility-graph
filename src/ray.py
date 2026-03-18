"""
ray.py
Lançamento de raios entre pontos no R².
Um raio é bloqueado se algum círculo obstáculo interceptar o segmento.
"""

from typing import Tuple, List
from circle import Circle


def ray_is_blocked(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    obstacles: List[Circle],
) -> bool:
    """
    Verifica se o segmento p1–p2 é bloqueado por algum obstáculo.

    Args:
        p1        : ponto de origem do raio
        p2        : ponto de destino do raio
        obstacles : lista de círculos que podem bloquear o raio

    Returns:
        True  — raio bloqueado (algum obstáculo está no caminho)
        False — raio livre (visibilidade direta entre p1 e p2)
    """
    return any(obs.intersects_segment(p1, p2) for obs in obstacles)