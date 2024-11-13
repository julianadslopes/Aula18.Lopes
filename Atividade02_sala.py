import os
import pandas as pd
import numpy as np

# A reunião exige que você apresente o total de casos mensais de estelionato e que investigue se há um padrão estável desses crimes ao longo do tempo. 

try:
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando os casos de estelionato     
    df_estelionato = df[["estelionato", "mes_ano"]]
    print (df_estelionato)

# Agrupando os casos por ano
    df_estelionato_mes_ano = df_estelionato.groupby(["mes_ano"]).sum(["estelionato"]).reset_index()
    print (df_estelionato_mes_ano)
    array_estelionato_mes_ano = np.array(df_estelionato_mes_ano["estelionato"])

# Média e mediana de casos por mês 
    media_casos = np.mean (array_estelionato_mes_ano)
    mediana_casos = np.median (array_estelionato_mes_ano)

    print (media_casos)
    print (mediana_casos)
except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()