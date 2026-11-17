# Análise de Inconsistências em Logs

Programa em Python que compara dois arquivos de log e procura sinais de adulteração.
Atividade do curso de Segurança Cibernética (SENAI).

## O que o programa verifica

**Comparando os dois logs** (o primeiro é o original):
- EXPORT desaparecido
- DELETE desaparecido
- Horário alterado
- IP alterado
- Outros eventos desaparecidos ou inseridos

**Dentro de cada log:**
- LOGOUT sem LOGIN
- Usuário ativo após logout
- Registros fora de ordem

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `inconsistencias.txt` | lista de todas as inconsistências encontradas |
| `grafico_barras.png` | quantidade de LOGIN, VIEW, DOWNLOAD, UPDATE, CREATE_USER, CHANGE_PASSWORD e LOGOUT em cada log |
| `histograma_horarios.png` | frequência de eventos por horário (intervalos de 5 minutos), um gráfico para cada log |

## Como usar

```bash
pip install matplotlib
python src/analise_logs.py log_original.txt log_alterado.txt   # gera o relatório .txt
python src/graficos.py log_original.txt log_alterado.txt       # gera os gráficos
```

O primeiro arquivo deve ser o log original e o segundo, o log a ser verificado.

## Formato esperado do log

```
2026-11-08 08:00:01 LOGIN user=ana ip=192.168.1.10
2026-11-08 08:05:50 VIEW user=ana page=/dashboard
2026-11-08 08:15:02 LOGOUT user=ana
```

Data, hora e ação vêm sempre nas três primeiras posições. Os demais campos usam
o formato `chave=valor` (`user`, `ip`, `page`, `file`, `table`...), e o IP aparece
apenas nas linhas de LOGIN.

## Estrutura do projeto

```
analise_logs.py   # leitura, comparação, verificações e relatório
graficos.py       # gráfico de barras e histogramas (matplotlib)
```

## Como funciona

1. Cada linha é lida e separada em data/hora, ação, usuário, IP e detalhes
   (página, arquivo, tabela).
2. As linhas que existem em um log e não no outro são comparadas:
   - mesmo usuário, ação e detalhe, mesmo IP, mas horário diferente → **horário alterado**
   - mesmo usuário, ação, detalhe e horário, mas IP diferente → **IP alterado**
   - EXPORT ou DELETE sem correspondente no outro log → **desaparecido**
   - outra ação sem correspondente → **evento desaparecido** ou **evento inserido**
3. Em cada log, o programa acompanha quem está logado para achar LOGOUT sem LOGIN
   e ações depois do logout, e compara cada horário com o da linha anterior para
   achar registros fora de ordem.

