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