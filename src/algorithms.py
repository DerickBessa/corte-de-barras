def corte_guloso(n, precos):
    restante = n
    cortes = []
    while restante > 0:
        melhor_razao = -1.0
        melhor_tam = 1
        for t in range(1, restante + 1):
            razao = precos[t - 1] / t
            if razao > melhor_razao:
                melhor_razao = razao
                melhor_tam = t
        cortes.append(melhor_tam)
        restante -= melhor_tam
    valor_total = sum(precos[t - 1] for t in cortes)
    return valor_total, cortes


def corte_forca_bruta(n, precos):
    if n == 0:
        return 0, []
    melhor_valor = -float('inf')
    melhor_cortes = []
    for i in range(1, n + 1):
        v_resto, c_resto = corte_forca_bruta(n - i, precos)
        valor = precos[i - 1] + v_resto
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_cortes = [i] + c_resto
    return melhor_valor, melhor_cortes


def corte_pd_memo(n, precos):
    memo_valor = {}
    memo_corte = {}

    def f(m):
        if m == 0:
            return 0
        if m in memo_valor:
            return memo_valor[m]
        melhor = -float('inf')
        melhor_primeiro = 1
        for i in range(1, m + 1):
            valor = precos[i - 1] + f(m - i)
            if valor > melhor:
                melhor = valor
                melhor_primeiro = i
        memo_valor[m] = melhor
        memo_corte[m] = melhor_primeiro
        return melhor

    valor_total = f(n)
    cortes = []
    resto = n
    while resto > 0:
        c = memo_corte[resto]
        cortes.append(c)
        resto -= c
    return valor_total, cortes
