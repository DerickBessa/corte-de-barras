import time
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms import corte_guloso, corte_forca_bruta, corte_pd_memo
from generators import gerar_tabela_precos


def medir_tempo(algoritmo, n, precos_list):
    tempos = []
    for precos in precos_list:
        inicio = time.perf_counter()
        algoritmo(n, precos)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return np.mean(tempos), np.std(tempos)


def rodar_benchmark():
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    graficos_dir = os.path.join(results_dir, "graficos")
    os.makedirs(graficos_dir, exist_ok=True)

    np.random.seed(123)
    NUM_AMOSTRAS = 10

    tamanhos_pequenos = list(range(5, 22, 2))
    tamanhos_grandes = list(np.linspace(10, 500, 20, dtype=int))
    tamanhos_grandes = [max(5, t) for t in tamanhos_grandes if t >= 5]

    print("=" * 60)
    print("BENCHMARK - Fase 1: Tamanhos pequenos (FB vs PD vs Guloso)")
    print("=" * 60)
    registros = []
    for n in tamanhos_pequenos:
        precos_list = [gerar_tabela_precos(n, seed=42 + i) for i in range(NUM_AMOSTRAS)]
        t_gul, s_gul = medir_tempo(corte_guloso, n, precos_list)
        t_fb, s_fb = medir_tempo(corte_forca_bruta, n, precos_list)
        t_pd, s_pd = medir_tempo(corte_pd_memo, n, precos_list)
        registros.append((n, "guloso", t_gul, s_gul))
        registros.append((n, "forca_bruta", t_fb, s_fb))
        registros.append((n, "pd_memo", t_pd, s_pd))
        print(f"  n={n:2d}  Guloso={t_gul:.6f}s  FB={t_fb:.6f}s  PD={t_pd:.6f}s")

    print("\n" + "=" * 60)
    print("BENCHMARK - Fase 2: Tamanhos grandes (Guloso vs PD)")
    print("=" * 60)
    for n in tamanhos_grandes:
        precos_list = [gerar_tabela_precos(n, seed=42 + i) for i in range(NUM_AMOSTRAS)]
        t_gul, s_gul = medir_tempo(corte_guloso, n, precos_list)
        t_pd, s_pd = medir_tempo(corte_pd_memo, n, precos_list)
        registros.append((n, "guloso", t_gul, s_gul))
        registros.append((n, "pd_memo", t_pd, s_pd))
        print(f"  n={n:4d}  Guloso={t_gul:.6f}s  PD={t_pd:.6f}s")

    df = pd.DataFrame(registros, columns=["n", "algoritmo", "tempo_medio", "tempo_std"])
    csv_path = os.path.join(results_dir, "tempos.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nResultados salvos em: {csv_path}")
    return df


def gerar_graficos(df):
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    graficos_dir = os.path.join(results_dir, "graficos")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["figure.dpi"] = 150

    df_peq = df[df["n"] <= 21].copy()
    df_grd = df[df["n"] > 21].copy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    ax = axes[0]
    for alg in ["guloso", "forca_bruta", "pd_memo"]:
        sub = df_peq[df_peq["algoritmo"] == alg]
        ax.errorbar(sub["n"], sub["tempo_medio"], yerr=sub["tempo_std"],
                     marker="o", label=alg, capsize=3)
    ax.set_xlabel("Tamanho da barra (n)")
    ax.set_ylabel("Tempo medio (s)")
    ax.set_title("Pequeno: Guloso vs Forca Bruta vs PD")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    for alg in ["guloso", "pd_memo"]:
        sub = df_grd[df_grd["algoritmo"] == alg]
        ax.errorbar(sub["n"], sub["tempo_medio"], yerr=sub["tempo_std"],
                     marker="o", label=alg, capsize=3)
    ax.set_xlabel("Tamanho da barra (n)")
    ax.set_ylabel("Tempo medio (s)")
    ax.set_title("Grande: Guloso vs PD")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    tamanhos_plot = sorted(df_grd[df_grd["algoritmo"] == "pd_memo"]["n"].unique())
    diffs_por_n = {}
    for n in tamanhos_plot:
        for i in range(10):
            p = gerar_tabela_precos(n, seed=2000 + i * 100 + n)
            vg, _ = corte_guloso(n, p)
            vp, _ = corte_pd_memo(n, p)
            diffs_por_n.setdefault(n, []).append(vp - vg)
    ns = sorted(diffs_por_n.keys())
    medias = [np.mean(diffs_por_n[n]) for n in ns]
    stds = [np.std(diffs_por_n[n]) for n in ns]
    ax.bar([str(n) for n in ns], medias, yerr=stds, capsize=3, color="orange", alpha=0.7)
    ax.set_xlabel("Tamanho da barra (n)")
    ax.set_ylabel("Diferenca media (PD - Guloso) R$")
    ax.set_title("Quanto o Guloso perde vs PD")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path1 = os.path.join(graficos_dir, "comparacao_completa.png")
    plt.savefig(path1)
    print(f"Grafico salvo: {path1}")
    plt.close()

    return path1


if __name__ == "__main__":
    df = rodar_benchmark()
    gerar_graficos(df)
    print("Benchmark concluido.")
