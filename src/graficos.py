import sys
from collections import Counter

import matplotlib.pyplot as plt

from analise_logs import ler_log

ACOES = ["LOGIN", "VIEW", "DOWNLOAD", "UPDATE", "CREATE_USER", "CHANGE_PASSWORD", "LOGOUT"]


def grafico_barras(log1, log2, nome1, nome2):
    cont1 = Counter(e["acao"] for e in log1)
    cont2 = Counter(e["acao"] for e in log2)
    x = range(len(ACOES))

    plt.figure(figsize=(11, 5))
    plt.bar([i - 0.2 for i in x], [cont1[a] for a in ACOES], width=0.4, label=nome1, color="#2a78d6")
    plt.bar([i + 0.2 for i in x], [cont2[a] for a in ACOES], width=0.4, label=nome2, color="#eb6834")
    plt.xticks(list(x), ACOES, rotation=15)
    plt.ylabel("Quantidade")
    plt.title("Quantidade de eventos por tipo")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_barras.png")


def histograma(log1, log2, nome1, nome2):
    """Frequência de eventos ao longo do horário, em intervalos de 5 minutos."""
    def minutos(log):
        return [e["horario"].hour * 60 + e["horario"].minute for e in log]

    todos = minutos(log1) + minutos(log2)
    inicio = min(todos) // 5 * 5
    fim = max(todos) // 5 * 5 + 5
    intervalos = range(inicio, fim + 1, 5)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True, sharey=True)
    ax1.hist(minutos(log1), bins=intervalos, color="#2a78d6", edgecolor="white")
    ax1.set_title(f"Eventos por horário - {nome1}")
    ax2.hist(minutos(log2), bins=intervalos, color="#eb6834", edgecolor="white")
    ax2.set_title(f"Eventos por horário - {nome2}")

    marcas = range(inicio, fim + 1, 10)
    ax2.set_xticks(list(marcas), [f"{m // 60:02d}:{m % 60:02d}" for m in marcas], rotation=45)
    ax2.set_xlabel("Horário")
    ax1.set_ylabel("Eventos")
    ax2.set_ylabel("Eventos")
    plt.tight_layout()
    plt.savefig("histograma_horarios.png")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python graficos.py log1.txt log2.txt")
        sys.exit(1)

    nome1, nome2 = sys.argv[1], sys.argv[2]
    log1 = ler_log(nome1)
    log2 = ler_log(nome2)

    grafico_barras(log1, log2, nome1, nome2)
    histograma(log1, log2, nome1, nome2)
    print("Gráficos salvos: grafico_barras.png e histograma_horarios.png")
    plt.show()