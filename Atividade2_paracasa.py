# Consigo afirmar que todas as delegacias (CISP) possuem um padrão médio de recuperação de veículo ou isso é meio disperso? Será que existe um padrão predominante ou não? 
import os
import pandas as pd
import numpy as np

os.system("cls")

try:
# Obtendo os dados    
    print ("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando as variáveis    
    df_recuperacao_veiculos = df_ocorrencias[["cisp", "recuperacao_veiculos"]]

# Totalizando recuperação de veículos por delegacia
    df_recuperacao_veiculos = df_recuperacao_veiculos.groupby(["cisp"]).sum(["recuperacao_veiculos"]).reset_index()
    print(df_recuperacao_veiculos.head())
    print("\nDados obtidos com sucesso!")

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print("*****************************************************************************************************")

# Gerando novos dados:
try: 
    print ("\n Calculando informações sobre padrão de recuperação de veículos...")
#Array NumPy
    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos["recuperacao_veiculos"])
# Média de recuperação de veículos
    media_recuperacao_veiculos = np.mean(array_recuperacao_veiculos)
# Mediana de roubo_veiculo - Divide a distribuição em duas partes iguais
    mediana_recuperacao_veiculo = np.median(array_recuperacao_veiculos)
# Distância entre média e mediana para ver se o valor da média é aceitável
    distancia_media_mediana = abs(media_recuperacao_veiculos-mediana_recuperacao_veiculo)/mediana_recuperacao_veiculo

# Amplitude total: Quanto mais próximo de zero, maior a homegeneidade dos dados
    maximo = np.max (array_recuperacao_veiculos)
    minimo = np.min (array_recuperacao_veiculos)
    amplitude = maximo - minimo

# Quartis - método weibull
    q1 = np.quantile(array_recuperacao_veiculos, 0.25, method="weibull")
    q2 = np.quantile(array_recuperacao_veiculos, 0.50, method="weibull")
    q3 = np.quantile(array_recuperacao_veiculos, 0.75, method="weibull")
    iqr = q3-q1
    lim_superior = q3 + (1.5*iqr)
    lim_inferior = q1 - (1.5*iqr)

# Filtrando os outliers
    # Inferiores
    df_recuperacao_veiculos_outliers_inferiores = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"]< lim_inferior]
    # Superiores
    df_recuperacao_veiculos_outliers_superiores = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"]> lim_superior]

 # Delegacias com maior recuperação
    df_recuperacao_acima_q3 = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"] > q3]
# Meses de menores ocorrências
    df_recuperacao_abaixo_q1 = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"] < q1]   
    

    print (f'Média: {media_recuperacao_veiculos:.2f}')
    print (f'Mediana: {mediana_recuperacao_veiculo:.2f}')
    print (f'Distância entre média e mediana: {distancia_media_mediana:.2f}')
    print (f'Amplitude: {amplitude}')
    print (f'Mínimo: {minimo}')
    print (f'Limite Inferior: {lim_inferior}')
    print (f'Q1: {q1}')
    print (f'Q2: {q2}')
    print (f'Q3: {q3}')
    print (f'IQR: {iqr}')
    print (f'Limite Superior: {lim_superior}')
    print (f'Máximo: {maximo}')

    print("\n DELEGACIAS COM MAIS RECUPERAÇÕES:")
    print (df_recuperacao_acima_q3.sort_values(by="recuperacao_veiculos", ascending=False).head(5))
    print("\n DELEGACIAS COM MENOS RECUPERAÇÕES::")
    print (df_recuperacao_abaixo_q1.sort_values(by="recuperacao_veiculos", ascending=False).head(5))

except Exception as e:
    print (f'Erro ao obter informações sobre padrão de recuperação de veículos: {e}')
    exit()

# Respondendo as questões:
print (f"""A média de recuperação de veículos é {media_recuperacao_veiculos}, enquanto a mediana é {mediana_recuperacao_veiculo}. A distância relativa entre a média e a mediana é de {distancia_media_mediana}, o que indica que há uma forte assimetria na distribuição.
Além disso, a amplitude de {amplitude} e o intervalo interquartil (IQR) de {iqr} confirmam que os dados são bastante dispersos.
Portanto, não há um padrão uniforme entre as delegacias, e os valores de recuperação variam muito.""")

print (f"""Os valores estão concentrados abaixo de Q3 ({q3}), mas há delegacias com valores muito maiores que a média.
Isso significa que não existe um padrão predominante, e os dados refletem uma variação significativa.""")

print (f"""Sim, as delegacias com valores acima do limite superior ({lim_superior}) são consideradas outliers superiores, ou seja, delegacias que fogem ao padrão por recuperar muito mais veículos do que a maioria.
As delegacias 59, 39, 21, 34 e 64 recuperaram muito mais veículos do que as outras, com valores de recuperação variando de 19437 a 29429. Essas são as delegacias que mais se destacam no estado.""")

print (f"""As delegacias com valores abaixo de Q1 ({q1}) são as que têm as menores recuperações. Essas delegacias apresentam níveis de recuperação muito baixos em relação às demais.""")