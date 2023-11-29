import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
#A. Execução do arquivo; conversão do arquivo CSV para o DataFrame em uma lista:
df = pd.read_csv('ArquivoDadosProjeto.csv', sep=';')
dados = df.values.tolist()

print('Todos os dados:')
for linha in dados:
    print(linha)

#B. Leitura da data inicial e final declarada pelo usuário; Tomei liberdade de adicionar o input para recolher os dados de temperatura da divisão "C", para dividir entre perguntas e envio de dados para o usuário.
inicioData = datetime.strptime(input(
    'Declare o mês e o ano para que possa iniciar o filtro da precipitação atmosférica (MM/AAAA): '), '%m/%Y')
finalData = datetime.strptime(
    input('Declare o mês e o ano para que possa ser filtrado o final (MM/AAAA): '), '%m/%Y')
tempMaxima = input(
    'Declare o ano para que seja filtrada a maior temperatura da primeira semana de cada mês (AAAA): ')

for linha in dados:
    data = datetime.strptime(linha[0], '%d/%m/%Y')
    if inicioData <= data <= finalData:
        print(f'Na data de: {linha[0]}, a precipitação atmosférica foi de: {linha[1]} mm')

with open('ArquivoDadosProjeto.csv', mode='r') as arquivo_csv:
    csv_reader = csv.reader(arquivo_csv, delimiter=';')
    next(csv_reader)
#. Converte os dados de inicio e final de data:
    for mes in range(1, 13):
        inicioData = datetime.strptime(f'01/{mes}/{tempMaxima}', '%d/%m/%Y')
        finalData = datetime.strptime(f'07/{mes}/{tempMaxima}', '%d/%m/%Y')

        tempMax = None
        arquivo_csv.seek(0)
        next(csv_reader)
        for linha in csv_reader:
            #. Verifica se há um valor atribuido à linha e o converte para uma temperatura em número decimal.
            data = datetime.strptime(linha[0], '%d/%m/%Y')
            if inicioData <= data <= finalData:
                if isinstance(linha[2], str) and linha[2] != '':
                    temp = float(linha[2].replace(',', '.'))
                    if tempMax is None or temp > tempMax:
                        tempMax = temp
#C. O programa exibe a temperatura máxima dos primeiros 7 dias de cada mês:
        if tempMax is not None:
            print(
                f'A temperatura máxima da primeira semana de cada mês foi: mês {mes}: {tempMax:.1f} °C')
        else:
            print(
                f'Não há dados disponíveis para os primeiros 7 dias do mês {mes}')

# SEGUNDA FASE DO PROJETO:

#D. Analisando dados de precipitação; O programa cria um dicionário vazio para armazenar o volume de chuva de cada mês:

meses_chuvosos = {} 

for linha in dados:
    data = datetime.strptime(linha[0], '%d/%m/%Y')
    mes_ano = f'{data.month}/{data.year}'
    #. É somado o volume da chuva à entrada já existente no dicionário, e cria uma nova entrada para o mês:
    if mes_ano in meses_chuvosos:
        meses_chuvosos[mes_ano] += float(str(linha[1]).replace(',', '.'))
    else:
        meses_chuvosos[mes_ano] = float(str(linha[1]).replace(',', '.'))

#. Retorna a chave com maior valor no dicionário
mes_chuvoso = max(meses_chuvosos, key=meses_chuvosos.get)

print(
    f'O mês mais chuvoso foi: {mes_chuvoso} com {meses_chuvosos[mes_chuvoso]:.1f} mm de chuva')


#E. Apresenta média e moda da temperatura mínima, umidade do ar e velocidade do vento no mês de agosto nos ultimos 10 dias:

for ano in range(2006, 2017):
    dados_agosto = df[df['data'].str.contains(f'08/{ano}')]
    print(f'\nDados de agosto/{ano}:')
    if not dados_agosto.empty: #. Verifica se existem dados de agosto do ano em questão
        print(f'Média da temperatura mínima: {dados_agosto["minima"].mean():.1f} °C')
        print(f'Moda da temperatura mínima: {dados_agosto["minima"].mode()[0]:.1f} °C')
        print(f'Média da umidade do ar: {dados_agosto["um_relativa"].mean():.1f} %')
        print(f'Moda da umidade do ar: {dados_agosto["um_relativa"].mode()[0]:.1f} %')
        print(f'Média da velocidade do vento: {dados_agosto["vel_vento"].mean():.1f} km/h')
        print(f'Moda da velocidade do vento: {dados_agosto["vel_vento"].mode()[0]:.1f} km/h')
    else:
        print('Não há dados de agosto para este ano.')

#. Média e moda dos dados de todos os meses de agosto nos últimos 10 anos
dados_agosto = df[df['data'].str.contains('08/')]
print('\nDados de todos os meses de agosto nos últimos 10 anos:')
print(f'Média da temperatura mínima: {dados_agosto["minima"].mean():.1f} °C')
print(f'Moda da temperatura mínima: {dados_agosto["minima"].mode()[0]:.1f} °C')
print(f'Média da umidade do ar: {dados_agosto["um_relativa"].mean():.1f} %')
print(f'Moda da umidade do ar: {dados_agosto["um_relativa"].mode()[0]:.1f} %')
print(f'Média da velocidade do vento: {dados_agosto["vel_vento"].mean():.1f} km/h')
print(f'Moda da velocidade do vento: {dados_agosto["vel_vento"].mode()[0]:.1f} km/h')

#F. A década mais chuvosa:

# Identificando o separador do arquivo e carregando os dados do arquivo CSV:
with open('ArquivoDadosProjeto.csv', 'r') as f:
    first_line = f.readline()
    sep = ',' if ',' in first_line else ';'

df = pd.read_csv('ArquivoDadosProjeto.csv', sep=sep, parse_dates=['data'], index_col='data', date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y'))

# Filtrando os dados para excluir as linhas após 2016-07-10
df = df.loc[df.index <= '2016-07-10']

# Convertendo o index para DatetimeIndex e agrupando por década e somando as chuvas:
df.index = pd.to_datetime(df.index, format='%d/%m/%Y')

decadas = df.groupby(df.index.year // 10 * 10)['precip'].sum()

# Dividindo o volume de chuva de cada década pela quantidade de anos. Logo após identificando a década mais chuvosa:
anos_por_decada = [10] * (len(decadas) - 1) + [df.index[-1].year % 10 + 1]
chuvas_por_ano = decadas / anos_por_decada

decada_mais_chuvosa = chuvas_por_ano.idxmax()

print(f"A década mais chuvosa foi {decada_mais_chuvosa}-{decada_mais_chuvosa+9} com {chuvas_por_ano.loc[decada_mais_chuvosa]:.2f} mm de chuva por ano.")

# Calculando a média de chuvas de cada década e exibindo a média de chuvas de cada década:
medias_por_decada = decadas / anos_por_decada

for decada in medias_por_decada.index:
    print(f"Média de chuvas na década {decada}-{decada+9}: {medias_por_decada.loc[decada]:.2f} mm por ano")

#G. Gerando um grágico de barras com médias acumuladas por décadas:

# Identificando o separador do arquivo e lendo o arquivo contendo os dados:
with open('ArquivoDadosProjeto.csv', 'r') as f:
    first_line = f.readline()
    sep = ',' if ',' in first_line else ';'

df = pd.read_csv('ArquivoDadosProjeto.csv', sep=sep)

# Convertendo a coluna "data" para datetime:
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

# Calculando a média acumulada de chuva por década:
df['decada'] = pd.cut(df['data'], bins=pd.date_range(start='1960-12-31', end='2016-07-10', freq='10AS'), right=False)
df_decada = df.groupby('decada').sum().reset_index()
df_decada['decada'] = df_decada['decada'].astype(str).str.slice(0, 4)

# Criando o gráfico:
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(df_decada['decada'], df_decada['precip'], color='green')

# Configurando o gráfico
ax.set_xlabel('Décadas:')
ax.set_ylabel('Chuva acumulada (mm):')
ax.set_title('Média de chuva acumulada por década:')
plt.show()