# visibility-graph
Visibility graph for circles in R2 - Scientific Research
# Grafo de Visibilidade entre Círculos no R²

Sistema de grafos de visibilidade para círculos no plano R², implementado em Python como base para pesquisa científica.

## Descrição

Dado um conjunto de círculos no R², dizemos que dois círculos **se veem** quando não há nenhum outro círculo bloqueando o caminho entre eles. Este sistema classifica a visibilidade entre cada par de círculos em três categorias:

| Peso | Situação | Cor |
|------|----------|-----|
| 0 | Visibilidade total — caminho completamente livre | 🟢 Verde |
| 1 | Bloqueio parcial — alguns raios passam, outros são bloqueados | 🟡 Amarelo |
| 2 | Bloqueio total — nenhum raio alcança o destino | 🔴 Vermelho |

O resultado é um **grafo completo** onde cada nó é um círculo e cada aresta tem peso 0, 1 ou 2.

## Método

Para cada par de círculos (A, B):
1. Amostramos `n` pontos uniformes na fronteira de cada círculo
2. Lançamos raios entre todos os pares de pontos amostrados
3. Verificamos se algum círculo obstáculo intercepta cada raio
4. Classificamos a aresta com base na proporção de raios bloqueados

## Estrutura do Projeto
```
visibility-graph/
│
├── src/
│   ├── circle.py        # Representação paramétrica do círculo
│   ├── ray.py           # Teste de bloqueio de raios
│   ├── visibility.py    # Classificação 0, 1, 2 entre pares
│   └── graph.py         # Construção e visualização do grafo
│
├── tests/
│   └── test_visibility.py  # Testes unitários
│
├── main.py              # Demonstração dos cenários
├── requirements.txt
└── README.md
```

## Cenários de Demonstração

| Cenário | Descrição |
|---------|-----------|
| 1 | Um círculo — representação paramétrica |
| 2 | Dois círculos — visibilidade total |
| 3 | Três círculos — bloqueio parcial |
| 4 | Três círculos — visibilidade total |
| 5 | Três círculos — bloqueio total |
| 6 | Verificação geométrica básica |

## Requisitos

- Python 3.8+
- numpy
- matplotlib
- networkx
- pytest

## Instalação
```bash
git clone https://github.com/draritajeronimo/visibility-graph.git
cd visibility-graph
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

## Como Usar

### Executar todos os cenários
```bash
python main.py
```

### Executar os testes
```bash
pytest tests/ -v
```

### Usar como biblioteca
```python
import sys
sys.path.insert(0, 'src')

from circle import Circle
from graph import build_graph, plot_graph

c1 = Circle(center=(0.0, 0.0), radius=1.0, label="C1")
c2 = Circle(center=(4.0, 1.5), radius=1.0, label="C2")
c3 = Circle(center=(8.0, 0.0), radius=1.0, label="C3")

circles = [c1, c2, c3]
G = build_graph(circles, n_samples=64)
plot_graph(circles, G)
```

## Autores

- **Dra. Rita Jerônimo** — [@draritajeronimo](https://github.com/draritajeronimo)

## Licença

MIT License