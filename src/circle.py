"""
circle.py
Representação paramétrica de um círculo no R².

    x(t) = cx + r * cos(t)
    y(t) = cy + r * sin(t),  t ∈ [0, 2π)
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Circle:
    """
    Círculo no R² definido por centro e raio.

    Atributos:
        center : (cx, cy) — coordenadas do centro
        radius : r > 0    — raio
        label  : nome identificador (usado nos grafos)
    """
    center: Tuple[float, float]
    radius: float
    label: str = ""

    def __post_init__(self):
        if self.radius <= 0:
            raise ValueError(f"Raio deve ser positivo. Recebido: {self.radius}")
        self.center = (float(self.center[0]), float(self.center[1]))
        self.radius = float(self.radius)

    @property
    def cx(self) -> float:
        return self.center[0]

    @property
    def cy(self) -> float:
        return self.center[1]

    @property
    def area(self) -> float:
        """Área do círculo: A = π r²."""
        return np.pi * self.radius ** 2

    @property
    def perimeter(self) -> float:
        """Perímetro (circunferência): C = 2π r."""
        return 2 * np.pi * self.radius

    @property
    def bounding_box(self) -> Tuple[float, float, float, float]:
        """(x_min, y_min, x_max, y_max)"""
        return (
            self.cx - self.radius,
            self.cy - self.radius,
            self.cx + self.radius,
            self.cy + self.radius,
        )

    def point_at(self, t: float) -> Tuple[float, float]:
        """Ponto na fronteira para o ângulo t (em radianos)."""
        return (
            self.cx + self.radius * np.cos(t),
            self.cy + self.radius * np.sin(t),
        )

    def sample_boundary(self, n_points: int = 64) -> np.ndarray:
        """
        Retorna n_points pontos uniformemente espaçados na fronteira.
        Shape: (n_points, 2)
        """
        t = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
        x = self.cx + self.radius * np.cos(t)
        y = self.cy + self.radius * np.sin(t)
        return np.column_stack((x, y))

    def contains_point(self, point: Tuple[float, float]) -> bool:
        """True se o ponto estiver estritamente dentro do círculo."""
        dx = point[0] - self.cx
        dy = point[1] - self.cy
        return (dx ** 2 + dy ** 2) < self.radius ** 2

    def intersects_segment(
        self,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
    ) -> bool:
        """
        True se o segmento p1–p2 interceptar o interior do círculo.
        Usado em ray.py para detectar bloqueio.
        """
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        fx, fy = p1[0] - self.cx, p1[1] - self.cy

        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - self.radius ** 2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False

        sqrt_disc = np.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)

        return (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 < t2)

    def __repr__(self) -> str:
        lbl = f" '{self.label}'" if self.label else ""
        return f"Circle{lbl}(center=({self.cx}, {self.cy}), radius={self.radius})"