import numpy as np
from algorithms import corte_guloso, corte_forca_bruta, corte_pd_memo
from generators import gerar_tabela_precos, tabela_guloso_erra_n4


def verificar_corretude_fb_vs_pd(tamanhos_pequenos):
    print("=" * 60)
    print("VERIFICACAO: Forca Bruta vs PD (tamanhos pequenos)")
    print("=" * 60)
    erros = 0
    for n in tamanhos_pequenos:
        precos = gerar_tabela_precos(n, seed=42)
        v_fb, c_fb = corte_forca_bruta(n, precos)
        v_pd, c_pd = corte_pd_memo(n, precos)
        ok = "OK" if abs(v_fb - v_pd) < 1e-9 else "DIFERENTE"
        if ok == "DIFERENTE":
            erros += 1
        print(f"  n={n:3d}  FB={v_fb:8.2f}  PD={v_pd:8.2f}  {ok}")
    print(f"\nTotal de erros: {erros}\n")
    return erros == 0


def verificar_guloso_vs_pd(tamanhos):
    print("=" * 60)
    print("VERIFICACAO: Guloso vs PD (todos os tamanhos)")
    print("=" * 60)
    diferencas = []
    for n in tamanhos:
        precos = gerar_tabela_precos(n, seed=42)
        v_gul, c_gul = corte_guloso(n, precos)
        v_pd, c_pd = corte_pd_memo(n, precos)
        diff = v_pd - v_gul
        diferencas.append(diff)
        status = "OK" if diff >= -1e-9 else "ERRO (PD < Guloso)"
        if diff > 1e-9:
            status = f"GULOSO ERROU (diff={diff:.2f})"
        print(f"  n={n:4d}  Guloso={v_gul:8.2f}  PD={v_pd:8.2f}  {status}")

    if diferencas:
        media = np.mean(diferencas)
        desvio = np.std(diferencas)
        print(f"\nMedia da diferenca (PD - Guloso): {media:.4f}")
        print(f"Desvio padrao da diferenca:       {desvio:.4f}")
    print()
    return diferencas


def exemplo_guloso_erra():
    print("=" * 60)
    print("EXEMPLO CONCRETO: Onde o Guloso Erra")
    print("=" * 60)

    precos_n4 = tabela_guloso_erra_n4()
    n = len(precos_n4)
    print(f"Tabela de precos (n={n}) — classica do CLRS:")
    for i, p in enumerate(precos_n4):
        print(f"  Tamanho {i+1:2d}: R$ {p:6.2f}")
    print()

    v_gul, c_gul = corte_guloso(n, precos_n4)
    v_pd, c_pd = corte_pd_memo(n, precos_n4)

    guloso_detalhe = " + ".join(f"T{sz}(R${precos_n4[sz-1]:.0f})" for sz in c_gul)
    pd_detalhe = " + ".join(f"T{sz}(R${precos_n4[sz-1]:.0f})" for sz in c_pd)

    print(f"Guloso: valor = R$ {v_gul:.2f}, cortes = {c_gul} ({guloso_detalhe})")
    print(f"PD:     valor = R$ {v_pd:.2f}, cortes = {c_pd} ({pd_detalhe})")
    print(f"Diferenca (PD - Guloso): R$ {v_pd - v_gul:.2f}")
    print(f"O guloso perde R$ {v_pd - v_gul:.2f} por fazer uma escolha localista!")
    print()

    print("--- Buscando exemplo aleatorio onde guloso erra ---")
    encontrou = False
    for tentativa in range(500):
        seed_tent = 1000 + tentativa
        n_rand = np.random.RandomState(seed_tent).randint(6, 20)
        precos_rand = gerar_tabela_precos(n_rand, seed=seed_tent)
        vg, _ = corte_guloso(n_rand, precos_rand)
        vp, _ = corte_pd_memo(n_rand, precos_rand)
        if abs(vp - vg) > 0.5:
            print(f"\nEncontrado! (seed={seed_tent}, n={n_rand})")
            print(f"  Guloso = R$ {vg:.2f}, PD = R$ {vp:.2f}, diff = R$ {vp - vg:.2f}")
            print(f"  Precos: {precos_rand}")
            encontrou = True
            break
    if not encontrou:
        print("  Nenhum exemplo aleatorio encontrado com diff > 0.5 (guloso acertou em todos).")
    print()

    return precos_n4, v_gul, c_gul, v_pd, c_pd


if __name__ == "__main__":
    tamanhos_pequenos = list(range(5, 22, 2))
    verificar_corretude_fb_vs_pd(tamanhos_pequenos)

    tamanhos_todos = list(range(5, 101, 5))
    verificar_guloso_vs_pd(tamanhos_todos)

    exemplo_guloso_erra()
