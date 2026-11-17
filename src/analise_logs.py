import sys
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt


def ler_log(caminho):
    eventos = []
    with open(caminho, encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            partes = linha.split()
            if len(partes) < 3:
                continue  # pula linhas vazias ou incompletas

            # Campos no formato chave=valor (user=, ip=, page=, file=...)
            campos = {}
            for parte in partes[3:]:
                if "=" in parte:
                    chave, valor = parte.split("=", 1)
                    campos[chave] = valor

            eventos.append({
                "linha": numero,
                "horario": datetime.strptime(partes[0] + " " + partes[1], "%Y-%m-%d %H:%M:%S"),
                "acao": partes[2],
                "usuario": campos.pop("user", "-"),
                "ip": campos.pop("ip", "-"),
                "detalhe": " ".join(f"{k}={v}" for k, v in campos.items()),
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
            mesmo_evento = (e1["usuario"] == e2["usuario"] and e1["acao"] == e2["acao"]
                and e1["detalhe"] == e2["detalhe"])
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
        else:
            problemas.append(f"EVENTO DESAPARECIDO: linha {e1['linha']} -> {e1['texto']}")

    # O que sobrou no segundo log não existia no original
    for e2 in so_no_2:
        problemas.append(f"EVENTO INSERIDO: linha {e2['linha']} -> {e2['texto']}")

    return problemas


def verificar(eventos, nome):
    problemas = []
    logado = {}

    for e in eventos:
        usuario = e["usuario"]
        if e["acao"] == "LOGIN":
            logado[usuario] = True
        elif e["acao"] == "LOGOUT":
            if not logado.get(usuario):
                problemas.append(f"[{nome}] LOGOUT SEM LOGIN: linha {e['linha']} -> {e['texto']}")
            logado[usuario] = False
        elif logado.get(usuario) is False:
            problemas.append(f"[{nome}] USUÁRIO ATIVO APÓS LOGOUT: linha {e['linha']} -> {e['texto']}")

    for anterior, atual in zip(eventos, eventos[1:]):
        if atual["horario"] < anterior["horario"]:
            problemas.append(f"[{nome}] REGISTRO FORA DE ORDEM: linha {atual['linha']} -> {atual['texto']}")

    return problemas


def salvar_relatorio(problemas, caminho="inconsistencias.txt"):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE INCONSISTÊNCIAS\n")
        arquivo.write(f"Total encontrado: {len(problemas)}\n\n")
        for p in problemas:
            arquivo.write(p + "\n")
    print(f"Relatório salvo em {caminho} ({len(problemas)} inconsistências)")





if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python analise_logs.py log1.txt log2.txt")
        sys.exit(1)

    nome1, nome2 = sys.argv[1], sys.argv[2]
    log1 = ler_log(nome1)
    log2 = ler_log(nome2)

    problemas = comparar(log1, log2)
    problemas += verificar(log1, nome1)
    problemas += verificar(log2, nome2)
    salvar_relatorio(problemas)

  