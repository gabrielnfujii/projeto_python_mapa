import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster

# Caminho do arquivo PIB
caminho_arquivo2 = '/content/pibs (1).csv'

try:
  # Tenta ler o arquivo CSV
  dados2 = pd.read_csv(caminho_arquivo2)
  print(f"Arquivo {caminho_arquivo2} carregado com sucesso!")

  # Preenche valores ausentes com 0
  dados2.fillna(0, inplace=True)

except FileNotFoundError:
  print(f"Arquivo não encontrado: {caminho_arquivo2}")

except pd.errors.ParserError:
  print(f"Erro ao processar o arquivo: {caminho_arquivo2}")

except Exception as e:
  print(f"Ocorreu um erro: {e}")

# Caminho do arquivo de países
caminho_arquivo1 = '/content/countries.csv'

try:
  # Tenta ler o arquivo CSV
  dados1 = pd.read_csv(caminho_arquivo1, sep=',', header=0, encoding='utf-8')
  print(f"Arquivo {caminho_arquivo1} carregado com sucesso!")

  # Preenche valores ausentes com 0
  dados1.fillna(0, inplace=True)

except FileNotFoundError:
  print(f"Arquivo não encontrado: {caminho_arquivo1}")

except pd.errors.ParserError:
  print(f"Erro ao processar o arquivo: {caminho_arquivo1}")

except Exception as e:
  print(f"Ocorreu um erro: {e}")

# Processa dados de PIB
pibs = dados2[["country", "pib", "name"]]

# Remove pontos e vírgulas, converte para float
pibs['pib'] = pibs['pib'].str.replace('.', '').str.replace(',', '').astype(float)

# Encontra os maiores e menores PIBs
maiores_pibs = pibs.nlargest(10, "pib")
menores_pibs = pibs.nsmallest(10, "pib")

# Imprime as tabelas
print("10 Maiores PIBs:")
print(maiores_pibs[["name", "pib"]])

print("\n10 Menores PIBs:")
print(menores_pibs[["name", "pib"]])

# Gráfico de barras para maiores PIBs
maiores_pibs.plot.bar(x="name", y="pib", color='green', legend=False)
plt.title("10 Maiores PIBs")
plt.ylabel("PIB")
plt.show()

# Gráfico de barras para menores PIBs
menores_pibs.plot.bar(x="name", y="pib", color='red', legend=False)
plt.title("10 Menores PIBs")
plt.ylabel("PIB")
plt.show()


# Carrega os dados
dados_paises = pd.read_csv('/content/countries.csv')

# Renomeia colunas de PIB
pibs = pibs.rename(columns={'latitude': 'latitude_pibs', 'longitude': 'longitude_pibs'})

# Junta dados de PIB com dados de países
pibs = pd.merge(pibs, dados_paises[['country', 'latitude', 'longitude']], how='left', on='country')

# Verifica se as colunas 'latitude' e 'longitude' estão presentes após a junção
if 'latitude' not in pibs.columns or 'longitude' not in pibs.columns:
    raise KeyError("As colunas 'latitude' e 'longitude' não foram encontradas no DataFrame após a junção.")

# Divide o Dataset de PIBs em dois: maiores e menores PIBs
maiores_pibs = pibs.nlargest(10, 'pib')
menores_pibs = pibs.nsmallest(10, 'pib')

# Cria um mapa e ajusta as coordenadas iniciais
mapa = folium.Map(location=[0, 0], zoom_start=2)

# Cria um MarkerCluster para melhorar a performance com muitos marcadores
marcadores = MarkerCluster().add_to(mapa)

# Itera sobre o DataFrame dos maiores PIBs
for indice, linha in maiores_pibs.iterrows():
    if pd.isna(linha['latitude']) or pd.isna(linha['longitude']):
        continue

    # Adiciona marcadores para os maiores PIBs
    folium.Marker(
        location=[linha['latitude'], linha['longitude']],
        popup=f"<b>{linha['country']}</b><br>PIB: {linha['pib']}",
        icon=folium.Icon(color='green')  # Verde para os maiores
    ).add_to(marcadores)

# Itera sobre o DataFrame dos menores PIBs
for indice, linha in menores_pibs.iterrows():
    if pd.isna(linha['latitude']) or pd.isna(linha['longitude']):
        continue  # Pula esta iteração

 # Adiciona marcadores para os menores PIBs
    folium.Marker(
        location=[linha['latitude'], linha['longitude']],
        popup=f"<b>{linha['country']}</b><br>PIB: {linha['pib']}",
        icon=folium.Icon(color='red')   # Vermelho para os menores
    ).add_to(marcadores)

# Exibe o mapa
mapa
