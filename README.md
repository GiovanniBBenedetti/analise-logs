# Análise de Inconsistências em Logs

Programa em Python que compara dois arquivos de log e procura sinais de adulteração.
Atividade do curso de Segurança Cibernética (SENAI).

## O que o programa verifica

**Comparando os dois logs** (o primeiro é o original):
- EXPORT desaparecido
- DELETE desaparecido
- Horário alterado
- IP alterado

**Dentro de cada log:**
- LOGOUT sem LOGIN
- Usuário ativo após logout
- Registros fora de ordem

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `inconsistencias.txt` | lista de todas as inconsistências encontradas |
| `grafico_barras.png` | quantidade de LOGIN, VIEW, DOWNLOAD, UPDATE, CREATE_USER, CHANGE_PASSWORD e LOGOUT em cada log |
| `histograma_horarios.png` | frequência de eventos por horário, um gráfico para cada log |

## Como usar

```bash
pip install matplotlib
python analise_logs.py log1.txt log2.txt
```

O primeiro arquivo deve ser o log original e o segundo, o log a ser verificado.

## Formato esperado do log

```
2026-11-08 08:00:01 LOGIN user=ana ip=192.168.1.10
```

## Estrutura do projeto

```
analise_logs.py   # leitura, comparação, verificações e relatório
graficos.py       # gráfico de barras e histogramas (matplotlib)
```

## Como funciona

1. Cada linha é lida e separada em data/hora, ação, usuário e IP.
2. As linhas que existem em um log e não no outro são comparadas:
   - mesmo usuário, ação e IP, mas horário diferente → **horário alterado**
   - mesmo usuário, ação e horário, mas IP diferente → **IP alterado**
   - EXPORT ou DELETE sem correspondente no outro log → **desaparecido**
3. Em cada log, o programa acompanha quem está logado para achar LOGOUT sem LOGIN
   e ações depois do logout, e compara cada horário com o da linha anterior para
   achar registros fora de ordem.