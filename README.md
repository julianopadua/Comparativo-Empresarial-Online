# Análise Comparativa de Empresas com Streamlit

Este projeto é uma aplicação web desenvolvida em Python utilizando Streamlit para fornecer uma análise comparativa de indicadores financeiros de diferentes empresas e uma análise gráfica dos dados históricos das ações. Ela permite a visualização de diversos indicadores financeiros e a plotagem de gráficos interativos dos preços das ações ao longo do tempo. O objetivo é educacional, em que busco evoluir aplicando conhecimentos adquiridos em prática!

O projeto pode ser acessado em: https://comparativo-empresarial-online-nxur6nrttpah85tgt9qzj9.streamlit.app/

## Funcionalidades

- **Análise de Indicadores Financeiros**: Compara os principais indicadores financeiros de até 3 empresas.
- **Análise Gráfica de Ações**: Permite a visualização dos dados históricos dos preços das ações com gráficos interativos.
- **Dados Financeiros Traduzidos**: Utiliza a biblioteca `googletrans` para traduzir descrições de empresas para o português.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criar aplicações web interativas em Python.
- **yFinance**: Biblioteca para acessar dados financeiros da Yahoo Finance.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Matplotlib**: Biblioteca para criação de gráficos.
- **Googletrans**: Biblioteca para tradução de textos usando a API do Google Translate.

## Requisitos

- Python 3.7 ou superior.
- Virtualenv para gerenciamento de ambientes virtuais.

## Setup e Execução

### Passo 1: Clonar o Repositório

Clone o repositório para sua máquina local usando o comando:

```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### Passo 2: Criar e Ativar um Ambiente Virtual
Crie um ambiente virtual usando virtualenv e ative-o:

```sh
python -m venv .venv
```

Ativar o ambiente virtual no Windows

```sh
.venv\Scripts\activate
```

No macOS/Linux

```sh
source .venv/bin/activate
```

### Passo 3: Instalar as Dependências
Instale as dependências listadas no arquivo requirements.txt:

```sh
pip install -r requirements.txt
```

### Passo 4: Executar a Aplicação
Execute a aplicação Streamlit:

```sh
streamlit run analise_comparativa.py
```

A aplicação estará disponível no seu navegador padrão.

## Estrutura do Projeto
analise_comparativa.py: Script principal que contém a aplicação Streamlit.
requirements.txt: Lista de todas as dependências necessárias para rodar o projeto.
### Funcionalidades do Código
Entrada de Dados: O usuário insere os tickers das empresas separados por vírgula.
Análise Comparativa: Compara diversos indicadores financeiros das empresas inseridas e destaca os maiores valores.
Análise Gráfica: Permite ao usuário selecionar um intervalo de datas e visualizar os gráficos de preços históricos das ações das empresas selecionadas.

## Aviso
Este projeto é apenas para fins educacionais e de demonstração. Não deve ser utilizado como uma ferramenta de investimento. As informações fornecidas são baseadas em dados públicos e podem não ser precisas ou completas. Ademais, recomendo a procura de um profissional, caso você não seja, antes de realizar investimentos.

## Contribuições
Contribuições são bem-vindas! Se você quiser melhorar o projeto ou corrigir algum bug, sinta-se à vontade.
```
