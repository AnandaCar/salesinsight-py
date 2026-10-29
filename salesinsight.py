# RF01–RF03: gerar, ler, inspecionar e limpar.
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path
import json
import matplotlib.pyplot as plt


def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gero o dataset sintético do enunciado, incluindo datas inválidas."""
    # A semente mantém os sorteios reproduzíveis.
    random.seed(seed)
    np.random.seed(seed)
    produtos = ['Notebook', 'Smartphone', 'Tablet', 'Monitor', 'Teclado', 'Mouse', 'Headset']
    categorias = {'Notebook': 'Computadores', 'Smartphone': 'Celulares', 'Tablet': 'Celulares', 'Monitor': 'Computadores', 'Teclado': 'Perifericos', 'Mouse': 'Perifericos', 'Headset': 'Perifericos'}
    precos = {'Notebook': 3500, 'Smartphone': 2200, 'Tablet': 1800, 'Monitor': 1200, 'Teclado': 250, 'Mouse': 120, 'Headset': 350}
    regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']
    data_inicio = datetime(2025, 1, 1)
    dados = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime('%Y-%m-%d')
        cliente = f'Cliente_{random.randint(1, 50):03d}'
        # Datas inválidas fazem parte do gerador fornecido no enunciado.
        if random.random() < 0.03:
            data_txt = 'DATA INVALIDA'
        dados.append({'id_venda': i + 1, 'data_venda': data_txt, 'cliente': cliente,
                      'produto': produto, 'categoria': categoria,
                      'regiao': random.choice(regioes), 'quantidade': quantidade,
                      'preco_unitario': preco})
    return pd.DataFrame(dados)


def inspecionar_dados(df):
    """Mostro a estrutura do DataFrame sem modificar os dados."""
    print('Shape:', df.shape)
    print('Colunas:', list(df.columns))
    print('Tipos:\n', df.dtypes)
    print('Nulos:\n', df.isnull().sum())
    print('Primeiras linhas:\n', df.head().to_string(index=False))
    return df


def tratar_dados(df):
    """Retorna cópia limpa e contagens auditáveis; motivos podem se sobrepor."""
    limpo = df.copy()
    alteradas = pd.Series(False, index=df.index)
    relatorio = {'registros_iniciais': len(df)}
    textos_alterados = pd.Series(False, index=df.index)
    for coluna in ['cliente', 'produto', 'categoria', 'regiao', 'data_venda']:
        if pd.api.types.is_string_dtype(limpo[coluna]) or limpo[coluna].dtype == object:
            antes = limpo[coluna].copy()
            limpo[coluna] = limpo[coluna].str.strip()
            textos_alterados |= antes.fillna('') != limpo[coluna].fillna('')
    relatorio['linhas_texto_padronizado'] = int(textos_alterados.sum())
    alteradas |= textos_alterados
    antes_data = limpo['data_venda'].copy()
    limpo['data_venda'] = pd.to_datetime(antes_data, errors='coerce')
    invalidas = limpo['data_venda'].isna()
    convertidas = ~invalidas & ~antes_data.map(lambda x: isinstance(x, (datetime, pd.Timestamp)))
    relatorio['datas_convertidas'] = int(convertidas.sum())
    relatorio['datas_invalidas_removidas'] = int(invalidas.sum())
    alteradas |= convertidas
    for coluna, tipo in [('quantidade', int), ('preco_unitario', float)]:

        valores = pd.to_numeric(limpo.loc[~invalidas, coluna], errors='raise')
        if valores.isna().any() or not np.isfinite(valores).all():
            raise ValueError(f'{coluna}: valor ausente ou não finito; revisar a fonte.')
        if coluna == 'quantidade' and ((valores % 1 != 0).any() or (valores <= 0).any()):
            raise ValueError('Quantidade deve ser inteira e positiva.')
        if coluna == 'preco_unitario' and (valores < 0).any():
            raise ValueError('Preço não pode ser negativo.')
        mudaram = ~limpo.loc[~invalidas, coluna].map(lambda x: isinstance(x, (int, np.integer) if tipo is int else (float, np.floating)))
        relatorio[coluna + '_convertidos'] = int(mudaram.sum())
        alteradas.loc[mudaram.index] |= mudaram
    limpo = limpo.loc[~invalidas].copy()
    limpo['quantidade'] = limpo['quantidade'].astype(int)
    limpo['preco_unitario'] = limpo['preco_unitario'].astype(float)
    relatorio['linhas_alteradas_mantidas'] = int(alteradas.loc[limpo.index].sum())
    relatorio['linhas_sem_alteracao'] = int((~alteradas.loc[limpo.index]).sum())
    relatorio['registros_finais'] = len(limpo)
    if limpo.empty:
        raise ValueError('Nenhuma venda válida para analisar.')
    print('RELATÓRIO DE LIMPEZA:', json.dumps(relatorio, indent=2, ensure_ascii=False))
    return limpo, relatorio



# RF04–RF06 e RF08: transformar, agrupar e segmentar.
MESES = dict(enumerate(['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'], start=1))


def processar_coluna(df, coluna, funcao_transformacao, nome_saida=None):
    """Aplico a função recebida aos valores de uma coluna."""
    resultado = df.copy()
    resultado[nome_saida or f'{coluna}_transformado'] = resultado[coluna].apply(funcao_transformacao)
    return resultado


def criar_colunas(df):
    """Crio receita, calendário e faixas com operações vetorizadas."""
    resultado = df.copy()
    resultado['receita_total'] = resultado['quantidade'] * resultado['preco_unitario']
    resultado['mes'] = resultado['data_venda'].dt.month
    resultado['mes_nome'] = resultado['mes'].map(MESES)
    resultado['ano'] = resultado['data_venda'].dt.year
    resultado['trimestre'] = 'Q' + resultado['data_venda'].dt.quarter.astype(str)
    resultado['faixa_receita_item'] = 'Nao Classificado'
    condicoes = [resultado['receita_total'] < 500,
                 (resultado['receita_total'] >= 500) & (resultado['receita_total'] < 5000),
                 resultado['receita_total'] >= 5000]
    for condicao, faixa in zip(condicoes, ['Baixo Valor','Medio Valor','Alto Valor']):
        resultado.loc[condicao, 'faixa_receita_item'] = faixa

    resultado = processar_coluna(resultado, 'receita_total', lambda x: round(x / 1000, 2), 'receita_em_milhares')
    return resultado


def calcular_metricas(df):
    """Retorna tabelas agrupadas; ticket = receita média por venda válida."""
    metricas = {}
    metricas['por_mes'] = df.groupby(['ano','mes']).agg(receita_total=('receita_total','sum'), quantidade=('quantidade','sum'), n_vendas=('id_venda','size')).reset_index().sort_values(['ano','mes'])
    metricas['por_mes']['mes_nome'] = metricas['por_mes']['mes'].map(MESES)
    metricas['top_produtos'] = df.groupby('produto', as_index=False)['receita_total'].sum().sort_values('receita_total', ascending=False).head(5)
    metricas['por_categoria'] = df.groupby('categoria', as_index=False)['receita_total'].sum()
    metricas['por_regiao'] = df.groupby('regiao').agg(receita_total=('receita_total','sum'), ticket_medio=('receita_total','mean')).reset_index()
    metricas['por_trimestre'] = df.groupby(['ano','trimestre'], as_index=False)['receita_total'].sum()
    for nome, tabela in metricas.items():
        print('\n' + nome.upper())
        print(tabela.to_string(index=False, float_format=lambda x: f'{x:,.2f}'))
    return metricas


def segmentar_clientes(df):
    """Classifica gasto acumulado: Bronze <5000; Prata <=15000; Ouro >15000."""
    clientes = df.groupby('cliente')['receita_total'].sum().reset_index(name='total_gasto')
    clientes['segmento'] = clientes['total_gasto'].apply(lambda x: 'Bronze' if x < 5000 else ('Prata' if x <= 15000 else 'Ouro'))
    clientes = clientes.sort_values('total_gasto', ascending=False)
    print('\nTOP 10 CLIENTES\n', clientes.head(10).to_string(index=False))
    print('\nDISTRIBUIÇÃO\n', clientes['segmento'].value_counts())
    return clientes



# RF07: quatro figuras com cores consistentes e exportação em PNG.
from matplotlib.ticker import FuncFormatter
CORES = {'Computadores': '#2456A6', 'Celulares': '#D57824', 'Perifericos': '#25846B'}


def moeda_br(valor):
    """Formato um número com separadores monetários brasileiros."""
    return f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def desenhar_visao(ax, tipo, df, metricas):
    """Desenho uma visão em um eixo, reutilizável nas figuras e no painel."""
    if tipo == 'linha':
        tabela = metricas['por_mes']
        datas = pd.to_datetime(dict(year=tabela['ano'], month=tabela['mes'], day=1))
        ax.plot(datas, tabela['receita_total'], color='#2456A6', marker='o', linewidth=2)
        import matplotlib.dates as mdates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        ax.set(title='Receita mensal', xlabel='Mês / ano', ylabel='Receita (R$)')
        ax.tick_params(axis='x', rotation=40)
    elif tipo == 'barras':
        tabela = metricas['top_produtos'].sort_values('receita_total')
        ax.barh(tabela['produto'], tabela['receita_total'], color='#2456A6')
        ax.set(title='Top 5 produtos', xlabel='Receita (R$)', ylabel='Produto')
    elif tipo == 'dispersao':
        for categoria, grupo in df.groupby('categoria'):
            ax.scatter(grupo['quantidade'], grupo['receita_total'], label=categoria,
                       color=CORES.get(categoria, '#657384'), alpha=0.7, s=35, edgecolors='white', linewidths=0.4)
        ax.set(title='Quantidade × receita por venda', xlabel='Quantidade (unidades)', ylabel='Receita por venda (R$)')
        ax.legend(title='Categoria', fontsize=8)
    elif tipo == 'regiao':
        tabela = metricas['por_regiao'].sort_values('receita_total')
        ax.barh(tabela['regiao'], tabela['receita_total'], color='#25846B')
        ax.set(title='Receita por região', xlabel='Receita (R$)', ylabel='Região')
    else:
        raise ValueError('Visão desconhecida: ' + tipo)
    eixo = ax.xaxis if tipo in ['barras', 'regiao'] else ax.yaxis
    eixo.set_major_formatter(FuncFormatter(lambda valor, pos: moeda_br(valor)))
    ax.grid(axis='x' if tipo in ['barras', 'regiao'] else 'y', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return ax


def criar_visualizacoes(df, metricas, pasta='outputs/graficos', mostrar=False):
    """Salvo três figuras individuais e um painel 2×2 e retorno os caminhos."""
    destino = Path(pasta)
    destino.mkdir(parents=True, exist_ok=True)
    arquivos = []
    for tipo, nome in [('linha','receita_por_mes.png'), ('barras','top_produtos.png'), ('dispersao','quantidade_vs_receita.png')]:
        fig, ax = plt.subplots(figsize=(11, 5.5))
        desenhar_visao(ax, tipo, df, metricas)
        plt.tight_layout()
        caminho = destino / nome
        plt.savefig(caminho, dpi=150)
        arquivos.append(str(caminho))
        if mostrar:
            plt.show()
        plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    for ax, tipo in zip(axes.flat, ['linha','barras','dispersao','regiao']):
        desenhar_visao(ax, tipo, df, metricas)
    fig.suptitle('SalesInsight PY | Painel de vendas — dados sintéticos', fontsize=17, fontweight='bold')
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    caminho = destino / 'painel_resumo.png'
    plt.savefig(caminho, dpi=150)
    arquivos.append(str(caminho))
    if mostrar:
        plt.show()
    plt.close(fig)
    return arquivos



# RF09–RF10: exportações e coordenação do fluxo.
def calcular_estatisticas(df):
    """Retorna indicadores simples usando tipos nativos serializáveis."""
    return {
        'receita_total': round(float(df['receita_total'].sum()), 2),
        'quantidade_total': int(df['quantidade'].sum()),
        'numero_vendas': int(len(df)),
        'numero_clientes': int(df['cliente'].nunique()),
        'ticket_medio': round(float(df['receita_total'].mean()), 2)
    }


def exportar_resultados(metricas, clientes, estatisticas, relatorio, pasta='outputs'):
    """Escreve CSV/JSON e relê o JSON para conferir a gravação."""
    destino = Path(pasta)
    destino.mkdir(parents=True, exist_ok=True)
    metricas['por_mes'].to_csv(destino / 'metricas_por_mes.csv', index=False, encoding='utf-8-sig')
    clientes.to_csv(destino / 'segmentacao_clientes.csv', index=False, encoding='utf-8-sig')
    for nome in ['por_categoria', 'por_regiao', 'por_trimestre', 'top_produtos']:
        metricas[nome].to_csv(destino / f'{nome}.csv', index=False, encoding='utf-8-sig')
    with open(destino / 'estatisticas_gerais.json', 'w', encoding='utf-8') as arquivo:
        json.dump(estatisticas, arquivo, indent=4, ensure_ascii=False)
    with open(destino / 'estatisticas_gerais.json', 'r', encoding='utf-8') as arquivo:
        conferencia = json.load(arquivo)
    assert conferencia == estatisticas, 'JSON diferente dos indicadores calculados.'
    with open(destino / 'relatorio_limpeza.json', 'w', encoding='utf-8') as arquivo:
        json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)
    print('JSON gravado e lido:', conferencia)
    return conferencia


class AnalisadorDeVendas:
    """Coordeno funções simples; self identifica esta instância do analisador."""
    def __init__(self, pasta_saida='outputs'):
        self.pasta_saida = Path(pasta_saida)

    def carregar(self, caminho):
        """Leio o CSV e preservo a tabela bruta para comparação."""
        self.df_bruto = pd.read_csv(caminho)
        return self.df_bruto

    def transformar(self):
        """Limpa os registros e cria as colunas derivadas."""
        limpo, self.relatorio = tratar_dados(self.df_bruto)
        self.df = criar_colunas(limpo)
        return self.df

    def analisar(self):
        """Calculo tabelas agregadas, clientes e estatísticas gerais."""
        self.metricas = calcular_metricas(self.df)
        self.clientes = segmentar_clientes(self.df)
        self.estatisticas = calcular_estatisticas(self.df)
        return self.metricas

    def visualizar(self, mostrar=False):
        """Exporto as quatro figuras do projeto."""
        return criar_visualizacoes(self.df, self.metricas, self.pasta_saida / 'graficos', mostrar)

    def resumo(self):
        """Exporto os resultados e mostro os indicadores gerais."""
        exportar_resultados(self.metricas, self.clientes, self.estatisticas, self.relatorio, self.pasta_saida)
        print('Receita total: R$', moeda_br(self.estatisticas['receita_total']))
        print('Vendas válidas:', self.estatisticas['numero_vendas'])
        return self.estatisticas


def main(mostrar=False):
    """Executo as etapas em ordem e retorno o analisador."""
    caminho = Path('vendas.csv')
    if not caminho.exists():
        gerar_dataset_vendas().to_csv(caminho, index=False)
    analisador = AnalisadorDeVendas()
    analisador.carregar(caminho)
    inspecionar_dados(analisador.df_bruto)
    analisador.transformar()
    analisador.analisar()
    analisador.visualizar(mostrar)
    analisador.resumo()
    print('[CONCLUÍDO] Fluxo executado sem erros.')
    return analisador


if __name__ == '__main__':
    main()
