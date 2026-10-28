# RF01–RF03: gerar, ler, inspecionar e limpar.
import pandas as pd  # Importa os recursos utilizados nesta etapa.
import numpy as np  # Importa os recursos utilizados nesta etapa.
import random  # Importa os recursos utilizados nesta etapa.
from datetime import datetime, timedelta  # Importa os recursos utilizados nesta etapa.
from pathlib import Path  # Importa os recursos utilizados nesta etapa.
import json  # Importa os recursos utilizados nesta etapa.
import matplotlib.pyplot as plt  # Importa os recursos utilizados nesta etapa.


def gerar_dataset_vendas(n_registros=200, seed=42):  # Define uma função reutilizável com os parâmetros indicados.
    """Gera o dataset sintético do enunciado, incluindo datas inválidas."""
    random.seed(seed)  # Fixa a semente para reproduzir os mesmos sorteios.
    np.random.seed(seed)  # Fixa a semente para reproduzir os mesmos sorteios.
    produtos = ['Notebook', 'Smartphone', 'Tablet', 'Monitor', 'Teclado', 'Mouse', 'Headset']  # Calcula e guarda produtos para as próximas operações.
    categorias = {'Notebook': 'Computadores', 'Smartphone': 'Celulares', 'Tablet': 'Celulares', 'Monitor': 'Computadores', 'Teclado': 'Perifericos', 'Mouse': 'Perifericos', 'Headset': 'Perifericos'}  # Calcula e guarda categorias para as próximas operações.
    precos = {'Notebook': 3500, 'Smartphone': 2200, 'Tablet': 1800, 'Monitor': 1200, 'Teclado': 250, 'Mouse': 120, 'Headset': 350}  # Calcula e guarda precos para as próximas operações.
    regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']  # Calcula e guarda regioes para as próximas operações.
    data_inicio = datetime(2025, 1, 1)  # Calcula e guarda data_inicio para as próximas operações.
    dados = []  # Calcula e guarda dados para as próximas operações.
    for i in range(n_registros):  # Percorre os elementos, executando o bloco uma vez para cada item.
        produto = random.choice(produtos)  # Sorteia um item entre as opções disponíveis.
        categoria = categorias[produto]  # Calcula e guarda categoria para as próximas operações.
        quantidade = random.randint(1, 10)  # Sorteia um inteiro dentro dos limites inclusivos.
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)  # Calcula e guarda preco para as próximas operações.
        data = data_inicio + timedelta(days=random.randint(0, 364))  # Sorteia um inteiro dentro dos limites inclusivos.
        data_txt = data.strftime('%Y-%m-%d')  # Calcula e guarda data_txt para as próximas operações.
        cliente = f'Cliente_{random.randint(1, 50):03d}'  # Sorteia um inteiro dentro dos limites inclusivos.
        if random.random() < 0.03:  # Executa o bloco somente quando esta condição é verdadeira.
            data_txt = 'DATA INVALIDA'  # Calcula e guarda data_txt para as próximas operações.
        dados.append({'id_venda': i + 1, 'data_venda': data_txt, 'cliente': cliente,  # Acrescenta o novo elemento à lista.
                      'produto': produto, 'categoria': categoria,  # Completa os campos do registro ou as opções de classificação.
                      'regiao': random.choice(regioes), 'quantidade': quantidade,  # Sorteia um item entre as opções disponíveis.
                      'preco_unitario': preco})  # Completa os campos do registro ou as opções de classificação.
    return pd.DataFrame(dados)  # Devolve o resultado para quem chamou a função.


def inspecionar_dados(df):  # Define uma função reutilizável com os parâmetros indicados.
    """Mostra a estrutura do DataFrame e retorna os dados sem modificá-los."""
    print('Shape:', df.shape)  # Exibe o resultado para inspeção e aprendizagem.
    print('Colunas:', list(df.columns))  # Exibe o resultado para inspeção e aprendizagem.
    print('Tipos:\n', df.dtypes)  # Exibe o resultado para inspeção e aprendizagem.
    print('Nulos:\n', df.isnull().sum())  # Exibe o resultado para inspeção e aprendizagem.
    print('Primeiras linhas:\n', df.head().to_string(index=False))  # Exibe o resultado para inspeção e aprendizagem.
    return df  # Devolve o resultado para quem chamou a função.


def tratar_dados(df):  # Define uma função reutilizável com os parâmetros indicados.
    """Retorna cópia limpa e contagens auditáveis; motivos podem se sobrepor."""
    limpo = df.copy()  # Cria uma cópia para preservar a tabela original.
    alteradas = pd.Series(False, index=df.index)  # Inicia uma marcação falsa para cada linha da tabela.
    relatorio = {'registros_iniciais': len(df)}  # Calcula e guarda relatorio para as próximas operações.
    textos_alterados = pd.Series(False, index=df.index)  # Inicia uma marcação falsa para cada linha da tabela.
    for coluna in ['cliente', 'produto', 'categoria', 'regiao', 'data_venda']:  # Percorre os elementos, executando o bloco uma vez para cada item.
        if pd.api.types.is_string_dtype(limpo[coluna]) or limpo[coluna].dtype == object:  # Executa o bloco somente quando esta condição é verdadeira.
            antes = limpo[coluna].copy()  # Cria uma cópia para preservar a tabela original.
            limpo[coluna] = limpo[coluna].str.strip()  # Calcula e guarda limpo[coluna] para as próximas operações.
            textos_alterados |= antes.fillna('') != limpo[coluna].fillna('')  # Acumula as marcações sem contar a mesma linha duas vezes.
    relatorio['linhas_texto_padronizado'] = int(textos_alterados.sum())  # Soma valores ou conta condições verdadeiras.
    alteradas |= textos_alterados  # Acumula as marcações sem contar a mesma linha duas vezes.
    antes_data = limpo['data_venda'].copy()  # Cria uma cópia para preservar a tabela original.
    limpo['data_venda'] = pd.to_datetime(antes_data, errors='coerce')  # Converte os valores para datas que o Pandas consegue manipular.
    invalidas = limpo['data_venda'].isna()  # Identifica valores ausentes, inclusive datas inválidas convertidas em NaT.
    convertidas = ~invalidas & ~antes_data.map(lambda x: isinstance(x, (datetime, pd.Timestamp)))  # Aplica o mapeamento a cada valor da coluna.
    relatorio['datas_convertidas'] = int(convertidas.sum())  # Soma valores ou conta condições verdadeiras.
    relatorio['datas_invalidas_removidas'] = int(invalidas.sum())  # Soma valores ou conta condições verdadeiras.
    alteradas |= convertidas  # Acumula as marcações sem contar a mesma linha duas vezes.
    for coluna, tipo in [('quantidade', int), ('preco_unitario', float)]:  # Percorre os elementos, executando o bloco uma vez para cada item.
        # Validar apenas registros que permanecerão depois da remoção das datas.
        valores = pd.to_numeric(limpo.loc[~invalidas, coluna], errors='raise')  # Seleciona as linhas indicadas pela condição ou pelo índice.
        if valores.isna().any() or not np.isfinite(valores).all():  # Executa o bloco somente quando esta condição é verdadeira.
            raise ValueError(f'{coluna}: valor ausente ou não finito; revisar a fonte.')  # Interrompe a execução com uma mensagem para corrigir a entrada.
        if coluna == 'quantidade' and ((valores % 1 != 0).any() or (valores <= 0).any()):  # Executa o bloco somente quando esta condição é verdadeira.
            raise ValueError('Quantidade deve ser inteira e positiva.')  # Interrompe a execução com uma mensagem para corrigir a entrada.
        if coluna == 'preco_unitario' and (valores < 0).any():  # Executa o bloco somente quando esta condição é verdadeira.
            raise ValueError('Preço não pode ser negativo.')  # Interrompe a execução com uma mensagem para corrigir a entrada.
        mudaram = ~limpo.loc[~invalidas, coluna].map(lambda x: isinstance(x, (int, np.integer) if tipo is int else (float, np.floating)))  # Aplica o mapeamento a cada valor da coluna.
        relatorio[coluna + '_convertidos'] = int(mudaram.sum())  # Soma valores ou conta condições verdadeiras.
        alteradas.loc[mudaram.index] |= mudaram  # Seleciona as linhas indicadas pela condição ou pelo índice.
    limpo = limpo.loc[~invalidas].copy()  # Cria uma cópia para preservar a tabela original.
    limpo['quantidade'] = limpo['quantidade'].astype(int)  # Converte os valores para o tipo indicado.
    limpo['preco_unitario'] = limpo['preco_unitario'].astype(float)  # Converte os valores para o tipo indicado.
    relatorio['linhas_alteradas_mantidas'] = int(alteradas.loc[limpo.index].sum())  # Seleciona as linhas indicadas pela condição ou pelo índice.
    relatorio['linhas_sem_alteracao'] = int((~alteradas.loc[limpo.index]).sum())  # Seleciona as linhas indicadas pela condição ou pelo índice.
    relatorio['registros_finais'] = len(limpo)  # Calcula e guarda relatorio['registros_finais'] para as próximas operações.
    if limpo.empty:  # Executa o bloco somente quando esta condição é verdadeira.
        raise ValueError('Nenhuma venda válida para analisar.')  # Interrompe a execução com uma mensagem para corrigir a entrada.
    print('RELATÓRIO DE LIMPEZA:', json.dumps(relatorio, indent=2, ensure_ascii=False))  # Exibe o resultado para inspeção e aprendizagem.
    return limpo, relatorio  # Devolve o resultado para quem chamou a função.



# RF04–RF06 e RF08: transformar, agrupar e segmentar.
MESES = dict(enumerate(['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'], start=1))  # Calcula e guarda MESES para as próximas operações.


def processar_coluna(df, coluna, funcao_transformacao, nome_saida=None):  # Define uma função reutilizável com os parâmetros indicados.
    """Recebe uma função como argumento e a aplica a uma coluna."""
    resultado = df.copy()  # Cria uma cópia para preservar a tabela original.
    resultado[nome_saida or f'{coluna}_transformado'] = resultado[coluna].apply(funcao_transformacao)  # Aplica a função informada a cada valor.
    return resultado  # Devolve o resultado para quem chamou a função.


def criar_colunas(df):  # Define uma função reutilizável com os parâmetros indicados.
    """Cria receita, calendário e faixas com operações vetorizadas."""
    resultado = df.copy()  # Cria uma cópia para preservar a tabela original.
    resultado['receita_total'] = resultado['quantidade'] * resultado['preco_unitario']  # Calcula e guarda resultado['receita_total'] para as próximas operações.
    resultado['mes'] = resultado['data_venda'].dt.month  # Extrai um componente do calendário a partir das datas.
    resultado['mes_nome'] = resultado['mes'].map(MESES)  # Aplica o mapeamento a cada valor da coluna.
    resultado['ano'] = resultado['data_venda'].dt.year  # Extrai um componente do calendário a partir das datas.
    resultado['trimestre'] = 'Q' + resultado['data_venda'].dt.quarter.astype(str)  # Converte os valores para o tipo indicado.
    resultado['faixa_receita_item'] = 'Nao Classificado'  # Calcula e guarda resultado['faixa_receita_item'] para as próximas operações.
    condicoes = [resultado['receita_total'] < 500,  # Calcula e guarda condicoes para as próximas operações.
                 (resultado['receita_total'] >= 500) & (resultado['receita_total'] < 5000),  # Continua as condições da classificação vetorizada.
                 resultado['receita_total'] >= 5000]  # Completa a instrução iniciada nas linhas anteriores.
    for condicao, faixa in zip(condicoes, ['Baixo Valor','Medio Valor','Alto Valor']):  # Percorre os elementos, executando o bloco uma vez para cada item.
        resultado.loc[condicao, 'faixa_receita_item'] = faixa  # Seleciona as linhas indicadas pela condição ou pelo índice.
    # Segundo contexto de lambda: escala monetária, diferente da segmentação.
    resultado = processar_coluna(resultado, 'receita_total', lambda x: round(x / 1000, 2), 'receita_em_milhares')  # Calcula e guarda resultado para as próximas operações.
    return resultado  # Devolve o resultado para quem chamou a função.


def calcular_metricas(df):  # Define uma função reutilizável com os parâmetros indicados.
    """Retorna tabelas agrupadas; ticket = receita média por venda válida."""
    metricas = {}  # Calcula e guarda metricas para as próximas operações.
    metricas['por_mes'] = df.groupby(['ano','mes']).agg(receita_total=('receita_total','sum'), quantidade=('quantidade','sum'), n_vendas=('id_venda','size')).reset_index().sort_values(['ano','mes'])  # Agrupa registros e calcula a medida de cada grupo.
    metricas['por_mes']['mes_nome'] = metricas['por_mes']['mes'].map(MESES)  # Aplica o mapeamento a cada valor da coluna.
    metricas['top_produtos'] = df.groupby('produto', as_index=False)['receita_total'].sum().sort_values('receita_total', ascending=False).head(5)  # Agrupa registros e calcula a medida de cada grupo.
    metricas['por_categoria'] = df.groupby('categoria', as_index=False)['receita_total'].sum()  # Agrupa registros e calcula a medida de cada grupo.
    metricas['por_regiao'] = df.groupby('regiao').agg(receita_total=('receita_total','sum'), ticket_medio=('receita_total','mean')).reset_index()  # Agrupa registros e calcula a medida de cada grupo.
    metricas['por_trimestre'] = df.groupby(['ano','trimestre'], as_index=False)['receita_total'].sum()  # Agrupa registros e calcula a medida de cada grupo.
    for nome, tabela in metricas.items():  # Percorre os elementos, executando o bloco uma vez para cada item.
        print('\n' + nome.upper())  # Exibe o resultado para inspeção e aprendizagem.
        print(tabela.to_string(index=False, float_format=lambda x: f'{x:,.2f}'))  # Exibe o resultado para inspeção e aprendizagem.
    return metricas  # Devolve o resultado para quem chamou a função.


def segmentar_clientes(df):  # Define uma função reutilizável com os parâmetros indicados.
    """Classifica gasto acumulado: Bronze <5000; Prata <=15000; Ouro >15000."""
    clientes = df.groupby('cliente')['receita_total'].sum().reset_index(name='total_gasto')  # Agrupa registros e calcula a medida de cada grupo.
    clientes['segmento'] = clientes['total_gasto'].apply(lambda x: 'Bronze' if x < 5000 else ('Prata' if x <= 15000 else 'Ouro'))  # Aplica a função informada a cada valor.
    clientes = clientes.sort_values('total_gasto', ascending=False)  # Organiza as linhas conforme os valores da coluna.
    print('\nTOP 10 CLIENTES\n', clientes.head(10).to_string(index=False))  # Exibe o resultado para inspeção e aprendizagem.
    print('\nDISTRIBUIÇÃO\n', clientes['segmento'].value_counts())  # Exibe o resultado para inspeção e aprendizagem.
    return clientes  # Devolve o resultado para quem chamou a função.

