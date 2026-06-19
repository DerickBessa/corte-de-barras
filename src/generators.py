import numpy as np


def gerar_tabela_precos(n, seed=None):
    if seed is not None:
        np.random.seed(seed)
    preco_base = np.arange(1, n + 1, dtype=float)
    ruido = np.random.uniform(-0.5, 1.5, size=n)
    precos = preco_base + ruido
    precos = np.maximum(precos, 0.5 * np.arange(1, n + 1))
    precos = np.round(precos, 2).tolist()
    return precos


def tabela_com_erro_guloso():
    precos = [0.0] * 10
    precos[0] = 1.0
    precos[1] = 5.0
    precos[2] = 8.0
    precos[3] = 9.0
    precos[4] = 10.0
    precos[5] = 17.0
    precos[6] = 17.0
    precos[7] = 20.0
    precos[8] = 24.0
    precos[9] = 30.0
    return precos


def tabela_guloso_erra_n4():
    precos = [1.0, 5.0, 8.0, 9.0]
    return precos
