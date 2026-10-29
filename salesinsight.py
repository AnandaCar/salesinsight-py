# RF01–RF03: gerar, ler, inspecionar e limpar.
import pandas as pd  # Uso o Pandas para ler e analisar tabelas.
import numpy as np  # Uso o NumPy na semente e na validação de números finitos.
import random  # Faço os sorteios da base sintética.
from datetime import datetime, timedelta  # Defino a data inicial e somo dias às datas sorteadas.
from pathlib import Path  # Organizo os caminhos dos arquivos e das pastas.
import json  # Salvo e leio os indicadores no formato JSON.
import matplotlib.pyplot as plt  # Crio e exporto os gráficos.


def gerar_dataset_vendas(n_registros=200, seed=42):  # Defino uma função reutilizável com os parâmetros indicados.
    """Gero o dataset sintético do enunciado, incluindo datas inválidas."""
    random.seed(seed)  # Fixo a semente para reproduzir os mesmos sorteios.
    np.random.seed(seed)  # Fixo a semente para reproduzir os mesmos sorteios.
    produtos = ['Notebook', 'Smartphone', 'Tablet', 'Monitor', 'Teclado', 'Mouse', 'Headset']  # Defino os produtos que podem aparecer nas vendas.
    categorias = {'Notebook': 'Computadores', 'Smartphone': 'Celulares', 'Tablet': 'Celulares', 'Monitor': 'Computadores', 'Teclado': 'Perifericos', 'Mouse': 'Perifericos', 'Headset': 'Perifericos'}  # Relaciono cada produto à sua categoria.
    precos = {'Notebook': 3500, 'Smartphone': 2200, 'Tablet': 1800, 'Monitor': 1200, 'Teclado': 250, 'Mouse': 120, 'Headset': 350}  # Defino o preço de referência de cada produto.
    regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']  # Defino as cinco regiões possíveis.
    data_inicio = datetime(2025, 1, 1)  # Uso o primeiro dia de 2025 como referência.
    dados = []  # Inicio a lista que receberá os registros.
    for i in range(n_registros):  # Percorro os elementos, executando o bloco uma vez para cada item.
        produto = random.choice(produtos)  # Sorteio um item entre as opções disponíveis.
        categoria = categorias[produto]  # Busco a categoria do produto sorteado.
        quantidade = random.randint(1, 10)  # Sorteio um inteiro dentro dos limites inclusivos.
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)  # Vario o preço de referência entre 85% e 115% e arredondo para centavos.
        data = data_inicio + timedelta(days=random.randint(0, 364))  # Sorteio um dia dentro de 2025.
        data_txt = data.strftime('%Y-%m-%d')  # Escrevo a data no formato ano-mês-dia.
        cliente = f'Cliente_{random.randint(1, 50):03d}'  # Sorteio um dos 50 identificadores possíveis de cliente.
        if random.random() < 0.03:  # Insiro uma data inválida com probabilidade de 3% por registro.
            data_txt = 'DATA INVALIDA'  # Incluo o erro de data previsto para o exercício de limpeza.
        dados.append({'id_venda': i + 1, 'data_venda': data_txt, 'cliente': cliente,  # Acrescento o novo elemento à lista.
                      'produto': produto, 'categoria': categoria,  # Completo os campos do registro ou as opções de classificação.
                      'regiao': random.choice(regioes), 'quantidade': quantidade,  # Sorteio um item entre as opções disponíveis.
                      'preco_unitario': preco})  # Completo os campos do registro ou as opções de classificação.
    return pd.DataFrame(dados)  # Retorno o resultado para quem chamou a função.


def inspecionar_dados(df):  # Defino uma função reutilizável com os parâmetros indicados.
    """Mostro a estrutura do DataFrame sem modificar os dados."""
    print('Shape:', df.shape)  # Mostro o resultado para inspeção e aprendizagem.
    print('Colunas:', list(df.columns))  # Mostro o resultado para inspeção e aprendizagem.
    print('Tipos:\n', df.dtypes)  # Mostro o resultado para inspeção e aprendizagem.
    print('Nulos:\n', df.isnull().sum())  # Mostro o resultado para inspeção e aprendizagem.
    print('Primeiras linhas:\n', df.head().to_string(index=False))  # Mostro o resultado para inspeção e aprendizagem.
    return df  # Retorno o resultado para quem chamou a função.


def tratar_dados(df):  # Defino uma função reutilizável com os parâmetros indicados.
    """Retorna cópia limpa e contagens auditáveis; motivos podem se sobrepor."""
    limpo = df.copy()  # Crio uma cópia para preservar a tabela original.
    alteradas = pd.Series(False, index=df.index)  # Inicio uma marcação falsa para cada linha da tabela.
    relatorio = {'registros_iniciais': len(df)}  # Calculo e guardo relatorio para as próximas operações.
    textos_alterados = pd.Series(False, index=df.index)  # Inicio uma marcação falsa para cada linha da tabela.
    for coluna in ['cliente', 'produto', 'categoria', 'regiao', 'data_venda']:  # Percorro os elementos, executando o bloco uma vez para cada item.
        if pd.api.types.is_string_dtype(limpo[coluna]) or limpo[coluna].dtype == object:  # Executo o bloco somente quando esta condição é verdadeira.
            antes = limpo[coluna].copy()  # Crio uma cópia para preservar a tabela original.
            limpo[coluna] = limpo[coluna].str.strip()  # Removo espaços no início e no fim dos textos.
            textos_alterados |= antes.fillna('') != limpo[coluna].fillna('')  # Acumulo as marcações sem contar a mesma linha duas vezes.
    relatorio['linhas_texto_padronizado'] = int(textos_alterados.sum())  # Conto as linhas marcadas como verdadeiras.
    alteradas |= textos_alterados  # Acumulo as marcações sem contar a mesma linha duas vezes.
    antes_data = limpo['data_venda'].copy()  # Crio uma cópia para preservar a tabela original.
    limpo['data_venda'] = pd.to_datetime(antes_data, errors='coerce')  # Converto os valores para datas que o Pandas consegue manipular.
    invalidas = limpo['data_venda'].isna()  # Identifico valores ausentes, inclusive datas inválidas convertidas em NaT.
    convertidas = ~invalidas & ~antes_data.map(lambda x: isinstance(x, (datetime, pd.Timestamp)))  # Aplico o mapeamento a cada valor da coluna.
    relatorio['datas_convertidas'] = int(convertidas.sum())  # Conto as linhas marcadas como verdadeiras.
    relatorio['datas_invalidas_removidas'] = int(invalidas.sum())  # Conto as linhas marcadas como verdadeiras.
    alteradas |= convertidas  # Acumulo as marcações sem contar a mesma linha duas vezes.
    for coluna, tipo in [('quantidade', int), ('preco_unitario', float)]:  # Percorro os elementos, executando o bloco uma vez para cada item.
        # Validar apenas registros que permanecerão depois da remoção das datas.
        valores = pd.to_numeric(limpo.loc[~invalidas, coluna], errors='raise')  # Seleciono as linhas indicadas pela condição ou pelo índice.
        if valores.isna().any() or not np.isfinite(valores).all():  # Executo o bloco somente quando esta condição é verdadeira.
            raise ValueError(f'{coluna}: valor ausente ou não finito; revisar a fonte.')  # Interrompo a execução com uma mensagem para corrigir a entrada.
        if coluna == 'quantidade' and ((valores % 1 != 0).any() or (valores <= 0).any()):  # Executo o bloco somente quando esta condição é verdadeira.
            raise ValueError('Quantidade deve ser inteira e positiva.')  # Interrompo a execução com uma mensagem para corrigir a entrada.
        if coluna == 'preco_unitario' and (valores < 0).any():  # Executo o bloco somente quando esta condição é verdadeira.
            raise ValueError('Preço não pode ser negativo.')  # Interrompo a execução com uma mensagem para corrigir a entrada.
        mudaram = ~limpo.loc[~invalidas, coluna].map(lambda x: isinstance(x, (int, np.integer) if tipo is int else (float, np.floating)))  # Aplico o mapeamento a cada valor da coluna.
        relatorio[coluna + '_convertidos'] = int(mudaram.sum())  # Conto as linhas marcadas como verdadeiras.
        alteradas.loc[mudaram.index] |= mudaram  # Seleciono as linhas indicadas pela condição ou pelo índice.
    limpo = limpo.loc[~invalidas].copy()  # Crio uma cópia para preservar a tabela original.
    limpo['quantidade'] = limpo['quantidade'].astype(int)  # Converto os valores para o tipo indicado.
    limpo['preco_unitario'] = limpo['preco_unitario'].astype(float)  # Converto os valores para o tipo indicado.
    relatorio['linhas_alteradas_mantidas'] = int(alteradas.loc[limpo.index].sum())  # Seleciono as linhas indicadas pela condição ou pelo índice.
    relatorio['linhas_sem_alteracao'] = int((~alteradas.loc[limpo.index]).sum())  # Seleciono as linhas indicadas pela condição ou pelo índice.
    relatorio['registros_finais'] = len(limpo)  # Calculo e guardo relatorio['registros_finais'] para as próximas operações.
    if limpo.empty:  # Executo o bloco somente quando esta condição é verdadeira.
        raise ValueError('Nenhuma venda válida para analisar.')  # Interrompo a execução com uma mensagem para corrigir a entrada.
    print('RELATÓRIO DE LIMPEZA:', json.dumps(relatorio, indent=2, ensure_ascii=False))  # Mostro o resultado para inspeção e aprendizagem.
    return limpo, relatorio  # Retorno o resultado para quem chamou a função.



# RF04–RF06 e RF08: transformar, agrupar e segmentar.
MESES = dict(enumerate(['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'], start=1))  # Relaciono o número de cada mês ao nome em português.


def processar_coluna(df, coluna, funcao_transformacao, nome_saida=None):  # Defino uma função reutilizável com os parâmetros indicados.
    """Aplico a função recebida aos valores de uma coluna."""
    resultado = df.copy()  # Crio uma cópia para preservar a tabela original.
    resultado[nome_saida or f'{coluna}_transformado'] = resultado[coluna].apply(funcao_transformacao)  # Aplico a função informada a cada valor.
    return resultado  # Retorno o resultado para quem chamou a função.


def criar_colunas(df):  # Defino uma função reutilizável com os parâmetros indicados.
    """Crio receita, calendário e faixas com operações vetorizadas."""
    resultado = df.copy()  # Crio uma cópia para preservar a tabela original.
    resultado['receita_total'] = resultado['quantidade'] * resultado['preco_unitario']  # Multiplico a quantidade pelo preço unitário de cada venda.
    resultado['mes'] = resultado['data_venda'].dt.month  # Extraio um componente do calendário a partir das datas.
    resultado['mes_nome'] = resultado['mes'].map(MESES)  # Aplico o mapeamento a cada valor da coluna.
    resultado['ano'] = resultado['data_venda'].dt.year  # Extraio um componente do calendário a partir das datas.
    resultado['trimestre'] = 'Q' + resultado['data_venda'].dt.quarter.astype(str)  # Converto os valores para o tipo indicado.
    resultado['faixa_receita_item'] = 'Nao Classificado'  # Inicio a coluna antes de aplicar as três faixas.
    condicoes = [resultado['receita_total'] < 500,  # Calculo e guardo condicoes para as próximas operações.
                 (resultado['receita_total'] >= 500) & (resultado['receita_total'] < 5000),  # Continua as condições da classificação vetorizada.
                 resultado['receita_total'] >= 5000]  # Completo a instrução iniciada nas linhas anteriores.
    for condicao, faixa in zip(condicoes, ['Baixo Valor','Medio Valor','Alto Valor']):  # Percorro os elementos, executando o bloco uma vez para cada item.
        resultado.loc[condicao, 'faixa_receita_item'] = faixa  # Seleciono as linhas indicadas pela condição ou pelo índice.
    # Segundo contexto de lambda: escala monetária, diferente da segmentação.
    resultado = processar_coluna(resultado, 'receita_total', lambda x: round(x / 1000, 2), 'receita_em_milhares')  # Calculo e guardo resultado para as próximas operações.
    return resultado  # Retorno o resultado para quem chamou a função.


def calcular_metricas(df):  # Defino uma função reutilizável com os parâmetros indicados.
    """Retorna tabelas agrupadas; ticket = receita média por venda válida."""
    metricas = {}  # Guardo cada tabela de resultados em uma chave do dicionário.
    metricas['por_mes'] = df.groupby(['ano','mes']).agg(receita_total=('receita_total','sum'), quantidade=('quantidade','sum'), n_vendas=('id_venda','size')).reset_index().sort_values(['ano','mes'])  # Agrupo registros e calculo a medida de cada grupo.
    metricas['por_mes']['mes_nome'] = metricas['por_mes']['mes'].map(MESES)  # Aplico o mapeamento a cada valor da coluna.
    metricas['top_produtos'] = df.groupby('produto', as_index=False)['receita_total'].sum().sort_values('receita_total', ascending=False).head(5)  # Agrupo registros e calculo a medida de cada grupo.
    metricas['por_categoria'] = df.groupby('categoria', as_index=False)['receita_total'].sum()  # Agrupo registros e calculo a medida de cada grupo.
    metricas['por_regiao'] = df.groupby('regiao').agg(receita_total=('receita_total','sum'), ticket_medio=('receita_total','mean')).reset_index()  # Agrupo registros e calculo a medida de cada grupo.
    metricas['por_trimestre'] = df.groupby(['ano','trimestre'], as_index=False)['receita_total'].sum()  # Agrupo registros e calculo a medida de cada grupo.
    for nome, tabela in metricas.items():  # Percorro os elementos, executando o bloco uma vez para cada item.
        print('\n' + nome.upper())  # Mostro o resultado para inspeção e aprendizagem.
        print(tabela.to_string(index=False, float_format=lambda x: f'{x:,.2f}'))  # Mostro o resultado para inspeção e aprendizagem.
    return metricas  # Retorno o resultado para quem chamou a função.


def segmentar_clientes(df):  # Defino uma função reutilizável com os parâmetros indicados.
    """Classifica gasto acumulado: Bronze <5000; Prata <=15000; Ouro >15000."""
    clientes = df.groupby('cliente')['receita_total'].sum().reset_index(name='total_gasto')  # Agrupo registros e calculo a medida de cada grupo.
    clientes['segmento'] = clientes['total_gasto'].apply(lambda x: 'Bronze' if x < 5000 else ('Prata' if x <= 15000 else 'Ouro'))  # Aplico a função informada a cada valor.
    clientes = clientes.sort_values('total_gasto', ascending=False)  # Organizo as linhas conforme os valores da coluna.
    print('\nTOP 10 CLIENTES\n', clientes.head(10).to_string(index=False))  # Mostro o resultado para inspeção e aprendizagem.
    print('\nDISTRIBUIÇÃO\n', clientes['segmento'].value_counts())  # Mostro o resultado para inspeção e aprendizagem.
    return clientes  # Retorno o resultado para quem chamou a função.



# RF07: quatro figuras com cores consistentes e exportação em PNG.
from matplotlib.ticker import FuncFormatter  # Personalizo os valores monetários dos eixos.
CORES = {'Computadores': '#2456A6', 'Celulares': '#D57824', 'Perifericos': '#25846B'}  # Mantenho uma cor para cada categoria.


def moeda_br(valor):  # Defino uma função reutilizável com os parâmetros indicados.
    """Formato um número com separadores monetários brasileiros."""
    return f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')  # Retorno o resultado para quem chamou a função.


def desenhar_visao(ax, tipo, df, metricas):  # Defino uma função reutilizável com os parâmetros indicados.
    """Desenho uma visão em um eixo, reutilizável nas figuras e no painel."""
    if tipo == 'linha':  # Executo o bloco somente quando esta condição é verdadeira.
        tabela = metricas['por_mes']  # Calculo e guardo tabela para as próximas operações.
        datas = pd.to_datetime(dict(year=tabela['ano'], month=tabela['mes'], day=1))  # Converto os valores para datas que o Pandas consegue manipular.
        ax.plot(datas, tabela['receita_total'], color='#2456A6', marker='o', linewidth=2)  # Desenho a evolução temporal como uma linha.
        import matplotlib.dates as mdates  # Formato as datas no eixo do gráfico mensal.
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  # Configuro como os valores serão escritos no eixo.
        ax.set(title='Receita mensal', xlabel='Mês / ano', ylabel='Receita (R$)')  # Defino título e nomes dos eixos.
        ax.tick_params(axis='x', rotation=40)  # Inclino os rótulos para melhorar sua legibilidade.
    elif tipo == 'barras':  # Executo o bloco somente quando esta condição é verdadeira.
        tabela = metricas['top_produtos'].sort_values('receita_total')  # Organizo as linhas conforme os valores da coluna.
        ax.barh(tabela['produto'], tabela['receita_total'], color='#2456A6')  # Compara os totais usando barras horizontais.
        ax.set(title='Top 5 produtos', xlabel='Receita (R$)', ylabel='Produto')  # Defino título e nomes dos eixos.
    elif tipo == 'dispersao':  # Executo o bloco somente quando esta condição é verdadeira.
        for categoria, grupo in df.groupby('categoria'):  # Percorro os elementos, executando o bloco uma vez para cada item.
            ax.scatter(grupo['quantidade'], grupo['receita_total'], label=categoria,  # Desenho um ponto por venda, agrupado por categoria.
                       color=CORES.get(categoria, '#657384'), alpha=0.7, s=35, edgecolors='white', linewidths=0.4)  # Defino cores, transparência, tamanho e borda dos pontos.
        ax.set(title='Quantidade × receita por venda', xlabel='Quantidade (unidades)', ylabel='Receita por venda (R$)')  # Defino título e nomes dos eixos.
        ax.legend(title='Categoria', fontsize=8)  # Identifico as categorias representadas pelas cores.
    elif tipo == 'regiao':  # Executo o bloco somente quando esta condição é verdadeira.
        tabela = metricas['por_regiao'].sort_values('receita_total')  # Organizo as linhas conforme os valores da coluna.
        ax.barh(tabela['regiao'], tabela['receita_total'], color='#25846B')  # Compara os totais usando barras horizontais.
        ax.set(title='Receita por região', xlabel='Receita (R$)', ylabel='Região')  # Defino título e nomes dos eixos.
    else:  # Trato o caso em que as condições anteriores não foram atendidas.
        raise ValueError('Visão desconhecida: ' + tipo)  # Interrompo a execução com uma mensagem para corrigir a entrada.
    eixo = ax.xaxis if tipo in ['barras', 'regiao'] else ax.yaxis  # Calculo e guardo eixo para as próximas operações.
    eixo.set_major_formatter(FuncFormatter(lambda valor, pos: moeda_br(valor)))  # Configuro como os valores serão escritos no eixo.
    ax.grid(axis='x' if tipo in ['barras', 'regiao'] else 'y', alpha=0.2)  # Adiciono linhas discretas para facilitar a leitura.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)  # Removo bordas superiores e laterais desnecessárias.
    return ax  # Retorno o resultado para quem chamou a função.


def criar_visualizacoes(df, metricas, pasta='outputs/graficos', mostrar=False):  # Defino uma função reutilizável com os parâmetros indicados.
    """Salvo três figuras individuais e um painel 2×2 e retorno os caminhos."""
    destino = Path(pasta)  # Calculo e guardo destino para as próximas operações.
    destino.mkdir(parents=True, exist_ok=True)  # Crio as pastas de saída, caso ainda não existam.
    arquivos = []  # Calculo e guardo arquivos para as próximas operações.
    for tipo, nome in [('linha','receita_por_mes.png'), ('barras','top_produtos.png'), ('dispersao','quantidade_vs_receita.png')]:  # Percorro os elementos, executando o bloco uma vez para cada item.
        fig, ax = plt.subplots(figsize=(11, 5.5))  # Crio a figura e os eixos com tamanho explícito.
        desenhar_visao(ax, tipo, df, metricas)  # Reutilizo a função de desenho neste eixo.
        plt.tight_layout()  # Ajusto os espaços para evitar rótulos sobrepostos.
        caminho = destino / nome  # Calculo e guardo caminho para as próximas operações.
        plt.savefig(caminho, dpi=150)  # Exporto a figura em PNG com resolução de 150 dpi.
        arquivos.append(str(caminho))  # Acrescento o novo elemento à lista.
        if mostrar:  # Executo o bloco somente quando esta condição é verdadeira.
            plt.show()  # Mostro a figura no notebook.
        plt.close(fig)  # Libero a figura depois de exibir ou salvar.
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))  # Crio a figura e os eixos com tamanho explícito.
    for ax, tipo in zip(axes.flat, ['linha','barras','dispersao','regiao']):  # Percorro os elementos, executando o bloco uma vez para cada item.
        desenhar_visao(ax, tipo, df, metricas)  # Reutilizo a função de desenho neste eixo.
    fig.suptitle('SalesInsight PY | Painel de vendas — dados sintéticos', fontsize=17, fontweight='bold')  # Adiciono um título geral ao painel.
    plt.tight_layout(rect=(0, 0, 1, 0.95))  # Ajusto os espaços para evitar rótulos sobrepostos.
    caminho = destino / 'painel_resumo.png'  # Calculo e guardo caminho para as próximas operações.
    plt.savefig(caminho, dpi=150)  # Exporto a figura em PNG com resolução de 150 dpi.
    arquivos.append(str(caminho))  # Acrescento o novo elemento à lista.
    if mostrar:  # Executo o bloco somente quando esta condição é verdadeira.
        plt.show()  # Mostro a figura no notebook.
    plt.close(fig)  # Libero a figura depois de exibir ou salvar.
    return arquivos  # Retorno o resultado para quem chamou a função.



# RF09–RF10: exportações e coordenação do fluxo.
def calcular_estatisticas(df):
    """Retorna indicadores simples usando tipos nativos serializáveis."""
    return {  # Dicionário: cada chave identifica um indicador.
        'receita_total': round(float(df['receita_total'].sum()), 2),  # Somo as receitas das vendas válidas.
        'quantidade_total': int(df['quantidade'].sum()),  # Total de unidades vendidas.
        'numero_vendas': int(len(df)),  # Uma linha representa uma venda.
        'numero_clientes': int(df['cliente'].nunique()),  # Conta clientes distintos.
        'ticket_medio': round(float(df['receita_total'].mean()), 2)  # Receita média por venda.
    }


def exportar_resultados(metricas, clientes, estatisticas, relatorio, pasta='outputs'):
    """Escreve CSV/JSON e relê o JSON para conferir a gravação."""
    destino = Path(pasta)  # Representa a pasta de saída.
    destino.mkdir(parents=True, exist_ok=True)  # Crio a pasta se necessário.
    metricas['por_mes'].to_csv(destino / 'metricas_por_mes.csv', index=False, encoding='utf-8-sig')  # Sem índice artificial.
    clientes.to_csv(destino / 'segmentacao_clientes.csv', index=False, encoding='utf-8-sig')  # Preservo os acentos.
    for nome in ['por_categoria', 'por_regiao', 'por_trimestre', 'top_produtos']:  # Guardo as tabelas auxiliares.
        metricas[nome].to_csv(destino / f'{nome}.csv', index=False, encoding='utf-8-sig')  # Exporto cada tabela.
    with open(destino / 'estatisticas_gerais.json', 'w', encoding='utf-8') as arquivo:  # Abre em modo de escrita.
        json.dump(estatisticas, arquivo, indent=4, ensure_ascii=False)  # Salvo JSON legível.
    with open(destino / 'estatisticas_gerais.json', 'r', encoding='utf-8') as arquivo:  # Reabro em modo de leitura.
        conferencia = json.load(arquivo)  # Recupero os dados efetivamente salvos.
    assert conferencia == estatisticas, 'JSON diferente dos indicadores calculados.'  # Confiro integridade.
    with open(destino / 'relatorio_limpeza.json', 'w', encoding='utf-8') as arquivo:  # Guardo a auditoria.
        json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)  # Salvo contagens da limpeza.
    print('JSON gravado e lido:', conferencia)  # Mostro a conferência exigida.
    return conferencia  # Permito reutilizar o resultado.


class AnalisadorDeVendas:  # A classe reúne dados e operações do mesmo analisador.
    """Coordeno funções simples; self identifica esta instância do analisador."""
    def __init__(self, pasta_saida='outputs'):  # Inicializa um novo analisador.
        self.pasta_saida = Path(pasta_saida)  # Guardo onde salvar os resultados.

    def carregar(self, caminho):  # Recebo o caminho do CSV bruto.
        """Leio o CSV e preservo a tabela bruta para comparação."""
        self.df_bruto = pd.read_csv(caminho)  # Leio a tabela do disco.
        return self.df_bruto  # Retorno a tabela carregada.

    def transformar(self):  # Executo limpeza antes das novas colunas.
        """Limpa os registros e cria as colunas derivadas."""
        limpo, self.relatorio = tratar_dados(self.df_bruto)  # Recebo os dois retornos da limpeza.
        self.df = criar_colunas(limpo)  # Calculo receita, calendário e faixas.
        return self.df  # Retorno a tabela pronta para análise.

    def analisar(self):  # Coordeno as métricas e os segmentos.
        """Calculo tabelas agregadas, clientes e estatísticas gerais."""
        self.metricas = calcular_metricas(self.df)  # Agrupo as vendas em dimensões.
        self.clientes = segmentar_clientes(self.df)  # Classifica o gasto acumulado.
        self.estatisticas = calcular_estatisticas(self.df)  # Resume os indicadores.
        return self.metricas  # Retorno as tabelas agregadas.

    def visualizar(self, mostrar=False):  # Permito mostrar os gráficos no notebook.
        """Exporto as quatro figuras do projeto."""
        return criar_visualizacoes(self.df, self.metricas, self.pasta_saida / 'graficos', mostrar)  # Reutilizo o desenho.

    def resumo(self):  # Finaliza com arquivos e indicadores.
        """Exporto os resultados e mostro os indicadores gerais."""
        exportar_resultados(self.metricas, self.clientes, self.estatisticas, self.relatorio, self.pasta_saida)  # Salvo os arquivos e confiro o JSON.
        print('Receita total: R$', moeda_br(self.estatisticas['receita_total']))  # Formato para leitura.
        print('Vendas válidas:', self.estatisticas['numero_vendas'])  # Mostro o volume de registros.
        return self.estatisticas  # Retorno o resumo.


def main(mostrar=False):  # Ponto de entrada do programa.
    """Executo as etapas em ordem e retorno o analisador."""
    caminho = Path('vendas.csv')  # Uso arquivo na pasta atual de execução.
    if not caminho.exists():  # Preservo um dataset já existente.
        gerar_dataset_vendas().to_csv(caminho, index=False)  # Gero a base somente quando faltar.
    analisador = AnalisadorDeVendas()  # Crio um objeto que coordena a análise.
    analisador.carregar(caminho)  # Leio o CSV bruto.
    inspecionar_dados(analisador.df_bruto)  # Mostro a estrutura inicial.
    analisador.transformar()  # Trato os dados e acrescento as colunas da análise.
    analisador.analisar()  # Calculo as métricas e classifico os clientes.
    analisador.visualizar(mostrar)  # Salvo os gráficos.
    analisador.resumo()  # Exporto os relatórios.
    print('[CONCLUÍDO] Fluxo executado sem erros.')  # Confirma a execução completa.
    return analisador  # Permito validar os resultados depois.


if __name__ == '__main__':  # Executo automaticamente apenas quando este arquivo é o programa principal.
    main()  # Inicio o fluxo completo.

