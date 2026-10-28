# SalesInsight PY

Análise e visualização de vendas sintéticas — Módulo 1, até Semana 07.
Estudante: Ananda Carvalho. Desenvolvimento guiado com IA. Revise e compreenda todo o código antes da entrega. Commits automatizados são identificados como assistente.

## Objetivo
Analisar receita mensal/trimestral, produtos, categorias, regiões, clientes e quantidade × receita. Não utiliza modelos preditivos.

## Instalação e execução
Python 3.10+. Entre na pasta do projeto e execute:

    pip install -r requirements.txt
    python salesinsight.py

No Colab, abra salesinsight.ipynb e execute todas as células. O notebook de entrega é autossuficiente, sem depender do histórico de montagem. Também é possível enviar salesinsight.py e vendas.csv e executar !python salesinsight.py.
O programa usa vendas.csv da pasta atual. Se faltar, gera 200 registros com seed=42. Não substitui CSV existente. Saídas em outputs/.

## Estrutura
- salesinsight.py: funções e classe, código comentado.
- salesinsight.ipynb: explicações, código, saídas e gráficos.
- vendas.csv: dados brutos do gerador do enunciado.
- outputs/: CSVs, JSONs e graficos/ com quatro PNGs.
- VALIDACAO.md, KANBAN.md e ROTEIRO_VIDEO.md: verificação e apresentação.

## Dataset e regras
Cada linha é uma venda. Colunas: id_venda, data_venda, cliente, produto, categoria, regiao, quantidade, preco_unitario.
Receita = quantidade × preço unitário. Ticket médio = receita total / vendas válidas.
Faixa da receita: abaixo de R$ 500 = Baixo Valor; de R$ 500 até abaixo de R$ 5.000 = Medio Valor; a partir de R$ 5.000 = Alto Valor.
Segmento do gasto acumulado: abaixo de R$ 5.000 = Bronze; de R$ 5.000 até R$ 15.000 inclusive = Prata; acima de R$ 15.000 = Ouro.

## Limpeza e decisão técnica
200 entradas, 6 datas inválidas removidas, 194 datas convertidas e 194 saídas. Nenhum texto exigiu remoção de espaços. Quantidade e preço já tinham tipos corretos. As 194 linhas mantidas tiveram a data convertida: zero linhas totalmente inalteradas. Contagens por motivo podem se sobrepor.
A remoção ocorre antes de toda análise, mantendo a mesma base em todos os totais. Não fazemos imputação ou tratamento de outliers. Entradas numéricas inválidas interrompem o fluxo com mensagem. Em produção, a primeira opção seria recuperar as datas na fonte.

## Resultados
- Receita: R$ 1.380.210,31; ticket médio: R$ 7.114,49.
- 194 vendas, 1.035 unidades e 49 clientes.
- Notebook: R$ 493.242,63, líder entre produtos.
- Fevereiro: R$ 186.065,22, líder em receita; outubro: 25 vendas.
- Centro-Oeste: R$ 342.981,92, maior receita regional.
- Nordeste: R$ 8.653,08, maior ticket médio regional.
- Clientes: 35 Ouro, 9 Prata e 5 Bronze.
- Q1: R$ 436.911,45; Q2: R$ 243.915,54; Q3: R$ 343.009,31; Q4: R$ 356.374,01.
A simulação não representa uma empresa real. A dispersão não prova causalidade. Não há previsão de vendas.

## Conceitos aplicados
int, float, str, bool; listas, tuplas, dicionários; operadores e condições; repetições; funções com parâmetros, retorno e docstrings; lambdas em contextos distintos; função de ordem superior; módulos; datetime; CSV/JSON; DataFrames; filtros; groupby; Matplotlib; subplots; Git e branches; classe simples.
df.loc segue RF04; np.select é uma alternativa citada no enunciado. Kanban foi incluído para cobrir a orientação do vídeo, embora seja opcional.

## Referências e recursos auxiliares
Enunciado fornecido pela estudante, índice, trechos dos resumos e transcrições. Aulas 13–18: estruturas, Pandas, funções, lambda e manipulação. Aulas 19–21: gráficos. A classe é prevista no enunciado. Path e formatadores monetários são recursos auxiliares explicados no código. Ferramentas de empacotamento/teste não fazem parte da lógica de análise. Materiais privados do curso não estão no pacote de entrega.

## Validação e melhorias
Totais reconciliados; limites das faixas testados; JSON relido; CSV conferido; quatro PNGs em 150 dpi; script executado em processo novo e pasta vazia; notebook executado em kernel novo. Melhorias: recuperar datas na fonte, ampliar validação de esquema e testar CSVs externos autorizados.

## Git e entrega
Branches: main (entrega), develop (integração), feat/pipeline-dados (implementação), docs/readme (documentação). Mais de cinco commits reais preservados.
Publicação pública no GitHub depende de autorização da estudante. Submissão ao AVA pendente.

## Vídeo
PENDENTE: gravar vídeo de até 5 minutos e inserir link acessível do Drive ou YouTube não listado. Roteiro em ROTEIRO_VIDEO.md.
