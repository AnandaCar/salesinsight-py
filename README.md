# SalesInsight PY

Sou Ananda Carvalho e desenvolvi este projeto para aplicar os conteúdos do Módulo 1 do curso de IA para Análise Preditiva em uma análise de vendas. Organizei o fluxo desde a leitura da base até a exportação das tabelas e dos gráficos.

Meu objetivo foi entender como a receita varia ao longo do tempo, quais produtos e categorias geram mais receita, como as regiões se comportam e quais clientes acumulam maior gasto. Trabalhei com dados sintéticos, sem criar modelos preditivos.

## Como organizei o projeto
Retomei o Kanban apresentado na aula 01 e o versionamento das aulas 10 a 12. Separei as etapas em funções, como vimos nas aulas 15 e 16, para conseguir reutilizar o código e acompanhar melhor cada resultado.

- salesinsight.py: meu fluxo principal, com funções e classe.
- salesinsight.ipynb: explicações, código comentado, tabelas e gráficos.
- vendas.csv: base bruta gerada conforme o enunciado.
- outputs/: tabelas CSV, arquivos JSON e quatro gráficos PNG.
- MAPA_AULAS.md: relação entre o que desenvolvi e as aulas consultadas.
- VALIDACAO.md: verificações realizadas.
- KANBAN.md: organização das tarefas.

## Como executar
No Colab, abro salesinsight.ipynb e executo as células de cima para baixo. Esse ambiente foi apresentado na aula 03. O notebook de entrega funciona sem depender das variáveis de uma sessão anterior.

Para executar localmente, preciso de Python 3.10 ou superior. Dentro da pasta do projeto, uso:

    pip install -r requirements.txt
    python salesinsight.py

As bibliotecas principais são Pandas, NumPy e Matplotlib. Se vendas.csv não existir na pasta atual, o código gera a base. Se já existir, o arquivo é preservado. Os resultados ficam em outputs/.

## Base e limpeza
Usei o gerador do enunciado, com 200 registros e seed=42. Cada linha representa uma venda. As colunas são id_venda, data_venda, cliente, produto, categoria, regiao, quantidade e preco_unitario.

Com o Pandas, trabalhado nas aulas 13 e 14, conferi a estrutura antes de analisar. Retomando conversão de tipos, da aula 08, e datas, da aula 18, converti data_venda e removi as seis datas inválidas, conforme o RF03. Restaram 194 vendas.

Não encontrei espaços extras que precisassem de correção. Quantidade e preço já estavam nos tipos esperados. As 194 linhas mantidas tiveram a data convertida; nenhuma ficou totalmente sem alteração. As contagens por motivo podem se sobrepor, por isso não as somo como grupos independentes.

Minha decisão foi usar a mesma base limpa em todas as métricas. Não fiz imputação nem tratamento de outliers. Se surgirem números inválidos, o código interrompe a execução com uma mensagem. Em uma situação real, eu buscaria corrigir as datas na origem antes de excluir registros.

## Transformações e análise
Calculei receita_total como quantidade × preco_unitario, usando os operadores vistos na aula 04 e operações em colunas trabalhadas na aula 18. Extraí mês, trimestre e ano e usei um dicionário para escrever os meses em português.

Para a faixa de receita de cada venda, segui o RF04: abaixo de R$ 500 é Baixo Valor; de R$ 500 até abaixo de R$ 5.000 é Medio Valor; a partir de R$ 5.000 é Alto Valor. Usei df.loc; np.select seria uma alternativa, mas não precisava repetir a solução.

Com groupby, trabalhado na aula 18, calculei as métricas mensais, trimestrais, por produto, categoria e região. Considerei ticket médio como a receita média por venda válida.

Na segmentação, usei lambda, apresentada na aula 16. Somei o gasto de cada cliente e apliquei as regras do RF06: abaixo de R$ 5.000 é Bronze; de R$ 5.000 até R$ 15.000 inclusive é Prata; acima de R$ 15.000 é Ouro. Também usei lambda para mostrar receita em milhares, por meio de uma função que recebe outra função como argumento.

## Visualizações e exportação
Retomando as aulas 19 a 21, criei gráficos de linha, barras e dispersão. Reuni as visões em um painel 2×2 e exportei quatro PNGs em 150 dpi. Usei títulos, rótulos, legendas quando necessárias e cores consistentes.

Salvei métricas e clientes em CSV e estatísticas em JSON. Reli o JSON para conferir a gravação, conforme RF09. A aula 16 oferece o contexto de importação e exportação; os métodos e arquivos específicos seguem o enunciado.

## Resultados que encontrei
- Receita total: R$ 1.380.210,31.
- Ticket médio: R$ 7.114,49.
- 194 vendas válidas, 1.035 unidades e 49 clientes.
- Notebook liderou os produtos, com R$ 493.242,63.
- Fevereiro liderou a receita mensal, com R$ 186.065,22. Outubro teve mais vendas: 25.
- Centro-Oeste teve a maior receita regional: R$ 342.981,92. Nordeste teve o maior ticket médio: R$ 8.653,08.
- Classifiquei 35 clientes como Ouro, nove como Prata e cinco como Bronze.
- Receita trimestral: Q1 R$ 436.911,45; Q2 R$ 243.915,54; Q3 R$ 343.009,31; Q4 R$ 356.374,01.

Esses resultados descrevem somente a base sintética. Não representam uma empresa real nem permitem prever vendas futuras. A dispersão também não comprova causalidade: a receita depende da quantidade e do preço unitário.

## Validação e próximos cuidados
Conferi se os totais por mês, categoria, região, trimestre e cliente coincidiam. Testei os limites das faixas e dos segmentos, reli os arquivos e executei o script em processo novo e pasta vazia. O notebook também foi executado em kernel novo.

Como melhoria, eu recuperaria as datas inválidas na fonte, ampliaria a validação das colunas e testaria outras bases autorizadas. A classe e main atendem ao enunciado; não atribuí esses recursos a uma aula específica sem evidência. O MAPA_AULAS.md detalha as referências e os recursos auxiliares.

## Desenvolvimento e entrega
Projeto de Ananda Carvalho, desenvolvido com apoio de IA na implementação e na revisão.

Usei main para a entrega, develop para integração, feat/pipeline-dados para implementação e docs/readme para documentação. O histórico preserva mais de cinco commits reais.

## Meu vídeo
Link: pendente de gravação.
