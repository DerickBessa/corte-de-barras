# Corte de Barras — Análise de Algoritmos

Experimento comparativo de 3 algoritmos para o problema clássico de **Corte de Barras (Rod Cutting)**, desenvolvido para a disciplina de Análise de Algoritmos do IFCE.

## Algoritmos Implementados

| Algoritmo | Complexidade | Descrição |
|-----------|-------------|-----------|
| **Guloso** | O(n²) | Escolhe localmente o pedaço com melhor preço/tamanho. Não garante o ótimo global. |
| **Força Bruta** | O(2ⁿ) | Testa recursivamente todas as composições possíveis. Inviável para n > 25. |
| **PD (Memoização)** | O(n²) | Recursivo com memoização. Garante o valor ótimo e retorna os cortes. |

## Estrutura

```
corte-de-barras/
├── src/
│   ├── algorithms.py   — Implementação dos 3 algoritmos
│   ├── generators.py   — Geração de tabelas de preço
│   ├── verify.py       — Verificação de corretude
│   └── benchmark.py    — Medição de tempo e gráficos
├── notebooks/
│   └── analise.ipynb   — Relatório final com gráficos e discussão
├── results/
│   ├── tempos.csv      — Resultados das medições
│   └── graficos/       — Gráficos gerados
├── video/
│   └── link.txt        — Link do vídeo de apresentação
├── index.html          — Página explicativa com guia do vídeo
├── requirements.txt
└── README.md
```

## Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar corretude dos algoritmos
python src/verify.py

# Rodar benchmark completo
python src/benchmark.py

# Abrir o notebook
jupyter notebook notebooks/analise.ipynb
```

## Resultados

- A Força Bruta torna-se inviável a partir de n ≈ 25 devido à explosão exponencial.
- O Guloso é o mais rápido (O(n)) mas pode errar o valor ótimo.
- A PD resolve exatamente em O(n²) e escala bem até n > 500.
