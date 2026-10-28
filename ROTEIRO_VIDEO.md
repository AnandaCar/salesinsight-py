# Meu roteiro de apresentação — até 5 minutos

Planejei cerca de 4min50s. Vou ensaiar com o notebook aberto e ajustar as pausas ao tempo de execução. As referências são as aulas do meu índice, não a numeração das semanas.

## 0:00–0:30 | Objetivo e organização
Olá, eu sou Ananda Carvalho e este é o meu projeto SalesInsight PY. Minha proposta foi analisar uma base de vendas e organizar os resultados para entender o comportamento da receita, dos produtos, das regiões e dos clientes. Para organizar o trabalho, usei um Kanban, retomando a ideia apresentada na aula 01.

Na tela: README e Kanban.

## 0:30–1:05 | Ambiente e base
Desenvolvi o projeto no Google Colab, que começamos a utilizar na aula 03. Usei o gerador fornecido no enunciado, com 200 vendas e uma semente fixa, para reproduzir a mesma base. Nesse trecho, apliquei listas e repetição, trabalhadas nas aulas 09 e 12, e dicionários, vistos na aula 13. Com o Pandas, abordado nas aulas 13 e 14, organizei os dados em um DataFrame.

Na tela: início do notebook, gerador e primeiras linhas. Executar o fluxo completo.

## 1:05–1:45 | Inspeção e limpeza
Antes de calcular os resultados, conferi as colunas, os tipos e os valores nulos. A base não tinha campos vazios, mas tinha seis datas inválidas. Retomando conversão de tipos, da aula 08, e manipulação de datas, da aula 18, converti a coluna de datas. Segui o enunciado e removi os registros que não puderam ser convertidos. Assim, todas as análises usam as mesmas 194 vendas válidas.

Na tela: inspeção e relatório de limpeza.

## 1:45–2:30 | Receita, métricas e clientes
Calculei a receita multiplicando quantidade pelo preço unitário, aplicando os operadores que vimos na aula 04. Depois, usei operações em colunas e agrupamentos, trabalhados na aula 18, para calcular os totais por mês, produto, categoria e região. Na segmentação dos clientes, usei lambda, vista na aula 16. Os limites vieram do desafio: até abaixo de cinco mil é Bronze; de cinco mil a quinze mil é Prata; acima disso é Ouro. Portanto, quinze mil ainda pertence a Prata.

Na tela: receita_total, groupby e segmentação.

## 2:30–3:20 | Gráficos e interpretação
Nas aulas 19 e 20, trabalhamos visualizações, e na aula 21 vimos barras, dispersão e exportação dos gráficos. Aqui, usei linha para acompanhar a receita mensal, barras para comparar os produtos e dispersão para observar quantidade e receita. Também reuni as visões em um painel dois por dois, como pede o enunciado. Notebook foi o produto com maior receita e fevereiro foi o mês com maior faturamento. Como os dados são sintéticos, esses resultados descrevem a simulação, e não uma empresa real.

Na tela: quatro figuras, destacando o painel.

## 3:20–4:05 | Funções e arquivos
Para evitar repetir código, organizei as etapas em funções, retomando as aulas 15 e 16. Também incluí a classe AnalisadorDeVendas e a função main para coordenar o fluxo, conforme o enunciado. Salvei as métricas em CSV e as estatísticas em JSON. A exportação retoma o contexto da aula 16; a releitura com json.load atende ao RF09 e confirma o conteúdo gravado.

Na tela: funções, classe, main e JSON relido.

## 4:05–4:50 | Git, validação e melhorias
Usei main, develop, feat/pipeline-dados e docs/readme para organizar as etapas, aplicando o versionamento estudado nas aulas 10 a 12. O projeto foi desenvolvido com apoio de IA, e o histórico registra as etapas dessa construção. Na validação, os totais das tabelas coincidiram e o código executou do início ao fim. Como melhoria, eu buscaria recuperar as datas inválidas na origem e testar outras bases. O principal resultado foi reunir o conteúdo do módulo em uma análise que eu consigo acompanhar e explicar.

Na tela: branches, commits e validação.

## Antes de gravar
Vou revisar o código e adaptar qualquer frase que não represente minha compreensão. Preciso manter meu rosto visível, boa iluminação e voz clara. Depois de gravar, vou conferir duração e acesso por link, inserir o endereço no README e realizar a submissão no AVA.
