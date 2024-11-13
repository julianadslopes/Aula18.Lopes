import os
import pandas as pd
import numpy as np

os.system("cls")

# Obter dados:
try: 
    print ("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

# Encodings: utf-8, iso 8859, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_roubo_veiculo = df_ocorrencias[["munic", "roubo_veiculo"]]

# Totalizar roubo_veiculos por munic
    df_roubo_veiculo = df_roubo_veiculo.groupby(["munic"]).sum(["roubo_veiculo"]).reset_index()
    print(df_roubo_veiculo.head())
    print("\nDados obtidos com sucesso!")

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print("*****************************************************************************************************")
# Gerando novos dados:
try: 
    print ("\n Calculando informações sobre padrão de roubo de veículos...")
#Array NumPy
    array_roubo_veiculo = np.array(df_roubo_veiculo["roubo_veiculo"])
# Média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
# Mediana de roubo_veiculo - Divide a distribuição em duas partes iguais
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
# Distância entre média e mediana para ver se o valor da média é aceitável
    distancia_media_mediana = abs(media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo
# Amplitude total: Quanto mais próximo de zero, maior a homegeneidade dos dados
    maximo = np.max (array_roubo_veiculo)
    minimo = np.min (array_roubo_veiculo)
    amplitude = maximo - minimo
# Quartis - método weibull
    q1 = np.quantile(array_roubo_veiculo, 0.25, method="weibull")
    q2 = np.quantile(array_roubo_veiculo, 0.50, method="weibull")
    q3 = np.quantile(array_roubo_veiculo, 0.75, method="weibull")
    iqr = q3-q1
    lim_superior = q3 + (1.5*iqr)
    lim_inferior = q1 - (1.5*iqr)

# Filtrando os outliers
    # Inferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"]< lim_inferior]
    # Superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"]> lim_superior]


# PRINTS    
    print(f' Média: {media_roubo_veiculo:.2f}')
    print(f' Mediana: {mediana_roubo_veiculo:.2f}')
    print(f' Distância: {distancia_media_mediana:.2f}')
    print(f'Amplitude: {amplitude}')
    print('Mínimo:', minimo)
    print(f' Limite Inferior: {lim_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f' Limite Superior: {lim_superior}')
    print('Máximo: ', maximo)
    print ('\n Municípios com outliers inferiores: ')
    if len(df_roubo_veiculo_outliers_inferiores)==0:
        print ("Não existem outliers inferiores!")
    else:
        print (df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))
    print ('\n Municípios com outliers superiores: ')
    if len(df_roubo_veiculo_outliers_superiores)==0:
        print ("Não existem outliers superiores!")
    else:
        print (df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))  

except Exception as e:
    print (f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()