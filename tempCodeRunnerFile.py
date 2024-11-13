import os
import pandas as pd
import numpy as np

os.system("cls")


try:
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando os casos de estelionato     
    df_estelionato = df[["estelionato", "mes_ano"]]
    print (df_estelionato)
    print (df_estelionato.head())

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print(60 *"*")

try:

# Agrupando os casos por ano
    df_estelionato_mes_ano = df_estelionato.groupby(["mes_ano"]).sum().reset_index()
    print (df_estelionato_mes_ano)
    array_estelionato_mes_ano = np.array(df_estelionato_mes_ano["estelionato"])

# Média e mediana de casos por mês 
    media_casos = np.mean (array_estelionato_mes_ano)
    mediana_casos = np.median (array_estelionato_mes_ano)
    distancia_relativa = abs(media_casos - mediana_casos) / mediana_casos

    print (f'Média de casos mensais de estelionato: {media_casos}')
    print (f'Mediana de casos mensais de estelionato: {mediana_casos}')
    print (f'Distância relativa entre média e mediana: {distancia_relativa}')

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print(60 *"*")

print ("Os dados analisados sugerem assimetria considerável entre os dados, que pode ser reflexo de outliers e instabilidade no número de estelionatos ao longo dos meses ")