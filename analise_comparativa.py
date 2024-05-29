import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from googletrans import Translator

#obtem indicadores financeiros das empresas
#utilizei st.cache_data para manter a pagina mesmo com interacao do usuario
#e para evitar recalculos desnecessarios
@st.cache_data
def get_financial_indicators(tickers):
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker.strip())
            info = stock.info
            
            data[ticker] = {
                'P/VP': info.get('priceToBook', 'N/A'),
                'Rend. de Dividendos': info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
                'Margem EBITDA': info.get('ebitdaMargins', 'N/A'),
                'LPA (EPS)': info.get('trailingEps', 'N/A'),
                'ROA': info.get('returnOnAssets', 'N/A'),
                'ROE': info.get('returnOnEquity', 'N/A'),
                'Dívida/Equidade': info.get('debtToEquity', 'N/A'),
                'Margem Operacional': info.get('operatingMargins', 'N/A'),
                'Crescimento de Receita': info.get('revenueGrowth', 'N/A'),
                'Crescimento de Lucro': info.get('earningsGrowth', 'N/A'),
                'Preço/Vendas': info.get('priceToSalesTrailing12Months', 'N/A'),
                'PE Trailing': info.get('trailingPE', 'N/A'),
                'PE Forward': info.get('forwardPE', 'N/A'),
                'Revenue Growth': info.get('revenueGrowth', 'N/A'),
                'Earnings Growth': info.get('earningsGrowth', 'N/A'),
            }
        except Exception as e:
            st.warning(f"Erro ao obter dados para {ticker}: {e}")
    return pd.DataFrame(data).T


#obtem as descricoes das empresas, tambem com st.cache_data
@st.cache_data
def get_company_descriptions(tickers):
    descriptions = {}
    translator = Translator()
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker.strip())
            info = stock.info
            summary = info.get('longBusinessSummary', 'N/A')
            summary_translated = translator.translate(summary, src='en', dest='pt').text
            
            descriptions[ticker] = {
                'Nome': info.get('longName', 'N/A'),
                'Resumo': summary_translated,
                'Indústria': info.get('industry', 'N/A'),
                'Setor': info.get('sector', 'N/A'),
                'Funcionários': info.get('fullTimeEmployees', 'N/A'),
                'País': info.get('country', 'N/A'),
                'Site': info.get('website', 'N/A')
            }
        except Exception as e:
            st.warning(f"Erro ao obter dados para {ticker}: {e}")
    return descriptions

#funcao que obtem dados historicos das acoes, novamente com st.cache_data
@st.cache_data
def get_historical_data(ticker, start_date, end_date):
    df = yf.download(ticker.strip(), start=start_date, end=end_date)
    return df

#plotagem dos dados historicos do valor das acoes das empresas
#datas como argumentos, para que o usuario escolha o intervalo
def plot_historical_data(tickers, start_date, end_date):
    for ticker in tickers:
        df = get_historical_data(ticker, start_date, end_date)
        if not df.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(df['Close'], label=ticker)
            plt.title(f'Histórico de Preço das Ações - {ticker}')
            plt.xlabel('Data')
            plt.ylabel('Preço de Fechamento')
            plt.legend()
            st.pyplot(plt.gcf())
        else:
            st.warning(f"Sem dados históricos disponíveis para {ticker}.")

#funcao que destaca a celula com maior valor em cada linha
def highlight_max(s):
    s_numeric = pd.to_numeric(s, errors='coerce')
    is_max = s_numeric == s_numeric.max()
    return ['background-color: yellow' if v else '' for v in is_max]

#titulo
st.title('Análise Comparativa de Empresas')

#usuario insere quais tickers ele deseja analisar
tickers_input = st.text_input('Insira os tickers das empresas separados por vírgula (ex: GOOG, AAPL, MSFT)', '')

if 'tickers' not in st.session_state:
    st.session_state.tickers = []
if 'descriptions' not in st.session_state:
    st.session_state.descriptions = {}
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = pd.DataFrame()

if tickers_input:
    tickers = tickers_input.upper().split(',')
    
    #limite de 3 empresas, depois pegamos os dados com as respectivas funcoes
    if len(tickers) > 3:
        st.error('Por favor, insira no máximo 3 empresas.')
    else:
        if st.button('Analisar'):
            with st.spinner('Buscando dados...'):
                st.session_state.tickers = tickers
                st.session_state.descriptions = get_company_descriptions(tickers)
                st.session_state.financial_data = get_financial_indicators(tickers)

if st.session_state.tickers:
    for ticker in st.session_state.tickers:
        if ticker in st.session_state.descriptions:
            desc = st.session_state.descriptions[ticker]
            st.subheader(desc['Nome'])
            st.markdown(f"**Resumo:** {desc['Resumo']}")
            st.markdown(f"**Indústria:** {desc['Indústria']}")
            st.markdown(f"**Setor:** {desc['Setor']}")
            st.markdown(f"**Funcionários:** {desc['Funcionários']}")
            st.markdown(f"**País:** {desc['País']}")
            st.markdown(f"**Site:** {desc['Site']}")
            st.markdown("---")
        else:
            st.error(f"Dados não encontrados para {ticker}")
    
    #secao de comparativo, com descricao sobre a tabela e sobre o uso de indicadores
    st.subheader('Comparativo dos Indicadores')
    st.markdown('''
        Esta tabela apresenta uma comparação dos principais indicadores financeiros das empresas selecionadas. 
        Cada linha representa um indicador financeiro, e cada coluna representa uma empresa. As células em amarelo 
        destacam os valores mais altos para cada indicador específico.
        
        É importante observar que um valor maior em um indicador nem sempre significa um melhor desempenho. Por exemplo, 
        um alto índice de Dívida/Equidade pode indicar um maior nível de endividamento, o que pode ser um risco. Por outro lado, 
        um alto LPA (Lucro por Ação) geralmente é positivo, pois sugere maior lucratividade.
        
        Esta análise é superficial e serve como um ponto de partida para uma investigação mais detalhada dos indicadores financeiros. 
        Certifique-se de considerar o contexto e outros fatores antes de tomar decisões de investimento.
    ''')

    df = st.session_state.financial_data.T  #quero transpor o df, para que os indicadores sejam as linhas e as empresas sejam as colunas
    df_highlighted = df.style.apply(highlight_max, axis=1)
    st.dataframe(df_highlighted, width=1200, height=600)

#nova secao, com descricao sobre a analise de dados historicos
st.subheader('Analisando Dados Históricos')
st.markdown('''
    A análise gráfica de ações permite visualizar o comportamento histórico dos preços das ações, 
    identificando tendências e padrões que podem ser úteis para tomar decisões de investimento.
    Utilize os gráficos abaixo para observar como o valor das ações das empresas selecionadas variou ao longo do tempo.
    Você pode selecionar o intervalo de datas para uma análise mais personalizada.
''')

#aqui temos os inputs para o intervalo de datas
start_date = st.date_input('Data de início', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('Data de fim', value=pd.to_datetime('today'))

if st.session_state.tickers:
    if st.button('Plotar Dados Históricos'):
        plot_historical_data(st.session_state.tickers, start_date, end_date)

#legendas
st.markdown('''**Legenda:**\n
P/VP: Preço/Valor Patrimonial\n
Rend. de Dividendos: Rendimento de Dividendos\n
Margem EBITDA: Margem EBITDA\n
LPA (EPS): Lucro por Ação\n
ROA: Retorno sobre Ativos\n
ROE: Retorno sobre Patrimônio\n
Dívida/Equidade: Dívida sobre Patrimônio\n
Margem Operacional: Margem Operacional\n
Crescimento de Receita: Crescimento de Receita\n
Crescimento de Lucro: Crescimento de Lucro\n
Preço/Vendas: Preço sobre Vendas\n
PE Trailing: P/E Trailing\n
PE Forward: P/E Forward\n
Revenue Growth: Crescimento de Receita\n
Earnings Growth: Crescimento de Lucro\n''')

st.markdown('Desenvolvido por Juliano E. S. Pádua')
