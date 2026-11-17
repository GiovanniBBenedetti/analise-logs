import sys
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt


def ler_log(caminho):
    eventos = []
    with open(caminho, encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            partes = linha.split()
            if len(partes) < 5:
                continue  # pula linhas vazias ou incompletas
            eventos.append({
                "linha": numero,
                "horario": datetime.strptime(partes[0] + " " + partes[1], "%Y-%m-%d %H:%M:%S"),
                "acao": partes[2],
                "usuario": partes[3].replace("user=", ""),
                "ip": partes[4].replace("ip=", ""),
                "texto": linha.strip(),
            })
    return eventos



def comparar(log1, log2):
    problemas = []

    # Linhas que existem em um arquivo e não no outro
    textos1 = {e["texto"] for e in log1}
    textos2 = {e["texto"] for e in log2}
    so_no_1 = [e for e in log1 if e["texto"] not in textos2]
    so_no_2 = [e for e in log2 if e["texto"] not in textos1]

    for e1 in so_no_1:
        par = None
        for e2 in so_no_2:
            mesmo_evento = e1["usuario"] == e2["usuario"] and e1["acao"] == e2["acao"]
            if mesmo_evento and e1["ip"] == e2["ip"]:
                par = e2
                problemas.append(f"HORÁRIO ALTERADO: {e1['usuario']} {e1['acao']} "
                                 f"{e1['horario']} -> {e2['horario']} (linha {e1['linha']})")
                break
            if mesmo_evento and e1["horario"] == e2["horario"]:
                par = e2
                problemas.append(f"IP ALTERADO: {e1['usuario']} {e1['acao']} em {e1['horario']} "
                                 f"{e1['ip']} -> {e2['ip']} (linha {e1['linha']})")
                break

        if par:
            so_no_2.remove(par)
        elif e1["acao"] in ("EXPORT", "DELETE"):
            problemas.append(f"{e1['acao']} DESAPARECIDO: linha {e1['linha']} -> {e1['texto']}")

    return problemas