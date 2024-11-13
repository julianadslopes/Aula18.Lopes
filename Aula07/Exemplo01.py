import os
import pandas as pd
import numpy as np
import timeit

os.system("cls")


try:
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando os casos de estelionato     
    df_estelionato = df[["estelionato", "mes_ano"]]
# Agrupando os casos por ano
    df_estelionato_mes_ano = df_estelionato.groupby(["mes_ano"]).sum(["estelionato"]).reset_index()
    # print (df_estelionato_mes_ano)
    # print (df_estelionato.head())

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

# print(60 *"*")

try:

    array_estelionato_mes_ano = np.array(df_estelionato_mes_ano["estelionato"])
# Média e mediana de casos por mês 
    media_casos = np.mean (array_estelionato_mes_ano)
    mediana_casos = np.median (array_estelionato_mes_ano)
    distancia_relativa = abs(media_casos - mediana_casos) / mediana_casos


# Quartis
    q1 = np.quantile (array_estelionato_mes_ano, 0.25, method="weibull")
    q2 = np.quantile (array_estelionato_mes_ano, 0.50, method="weibull")
    q3 = np.quantile (array_estelionato_mes_ano, 0.75, method="weibull")

# Meses de maiores ocorrências
    df_mes_ano_acima_q3 = df_estelionato_mes_ano[df_estelionato_mes_ano["estelionato"] > q3]
# Meses de menores ocorrências
    df_mes_ano_abaixo_q1 = df_estelionato_mes_ano[df_estelionato_mes_ano["estelionato"] < q1]

# Prints
    print("\n MEDIDAS DE TENDÊNCIA CENTRAL")
    print (f'Média de casos mensais de estelionato: {media_casos}')
    print (f'Mediana de casos mensais de estelionato: {mediana_casos}')
    print (f'Distância relativa entre média e mediana: {distancia_relativa}')
    print("\n MEDIDAS DE POSIÇÃO")
    print ("Q1 (25%):", q1)
    print ("Q2 (50%):", q2)
    print ("Q3 (75%):", q3)

    print("\n MAIORES MESES E ANOS:")
    print (df_mes_ano_acima_q3.sort_values(by="estelionato", ascending=False))
    print("\n MENORES MESES E ANOS:")
    print (df_mes_ano_abaixo_q1.sort_values(by="estelionato", ascending=False))

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print(60 *"*")

print ("Os dados analisados sugerem assimetria considerável entre os dados, que pode ser reflexo de outliers e instabilidade no número de estelionatos ao longo dos meses ")

