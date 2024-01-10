from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import regex as re
from lxml import etree as et
from itertools import repeat
import csv
import random
import time
from tqdm import tqdm_notebook
import warnings
warnings.filterwarnings('ignore')


'''
Un agente de usuario es una cadena que identifica la aplicación y la versión del software que está realizando la solicitud a un servidor web. 
En el contexto del código que estamos revisando, se utiliza para enviar solicitudes HTTP a la página web que estamos extrayendo.
Cada elemento de la lista header_list representa un agente de usuario simulado para un navegador web específico. 
El objetivo de usar múltiples agentes de usuario es simular el comportamiento de diferentes navegadores y evitar ser bloqueado por el servidor debido a solicitudes automatizadas o scraping.
En resumen, esta parte del código ayuda a realizar scraping de manera más amigable y a evitar posibles bloqueos por parte del servidor
'''

# Lista de agentes de usuario
header_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]

# URL base para la página de juegos
base_url = 'https://www.backloggd.com/games/lib/popular?page='





# Lista para almacenar enlaces de juegos
game_links = []

# Número de páginas a considerar (ajústalo según tus necesidades)
for page_no in tqdm_notebook(range(5)):
    page_url = base_url + str(page_no)
    user_agent = random.choice(header_list)
    header = {"User-Agent": user_agent}
    webpage = requests.get(page_url, headers=header)
    
    # Verificar si la página se cargó correctamente
    if webpage.status_code == 200:
        # Utilizar BeautifulSoup para extraer enlaces de juegos de la página
        soup1 = BeautifulSoup(webpage.content, 'html.parser')
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
        g = soup2.find('div', {'class': 'row show-release toggle-fade'})
        games = g.find_all('div', {'class': 'col-2 my-2 px-1 px-md-2'})
        game_ref = [game.find('a').get('href') for game in games]
        game_links.extend(['https://www.backloggd.com' + ref for ref in game_ref])

# Imprimir la cantidad de enlaces de juegos obtenidos
print(len(game_links))




# Definir las columnas para el DataFrame
cols = ['Title', 'Release Date', 'Team', 'Rating', 'Times Listed', 'Number of Reviews', 'Genres', 'Summary', 'Reviews', 'Plays', 'Playing', 'Backlogs', 'Wishlist', 'Platforms']
backloggd = pd.DataFrame(columns=cols)

# Iterar sobre los enlaces de juegos para obtener información detallada
for link in tqdm_notebook(game_links):
    user_agent = random.choice(header_list)
    header = {"User-Agent": user_agent}
    webpage = requests.get(link, headers=header)

    # Verificar si la página se cargó correctamente
    if webpage.status_code == 200:
        soup1 = BeautifulSoup(webpage.content, 'html.parser')
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

        # Obtener información básica del juego (título, fecha de lanzamiento, equipos, calificación, etc.)
        title = soup2.find('div', {'class': 'col-auto pr-1'}).get_text().strip()
        release_date = ' '.join(soup2.find('div', {'class': 'col-auto mt-auto pr-0'}).get_text().strip().split()[-3:])
        # (Otras secciones existentes)

        # Nuevo código para obtener plataformas
        released_on_section = soup2.find('h3', {'id': 'released-on'})
        if released_on_section:
            platforms = released_on_section.find_next('ul').find_all('li')
            platforms_list = [platform.get_text(strip=True) for platform in platforms]
        else:
            platforms_list = []

        # Inicializar la variable row
        row = [title, release_date, teams, rating, nlists, nreviews, genres, summary, reviews]

        # Añadir la lista de plataformas a tu DataFrame
        row.extend(platforms_list)

        # (Código existente)

        # Añadir la fila al DataFrame
        backloggd.loc[len(backloggd.index)] = row

# Imprimir las últimas filas del DataFrame resultante
print(backloggd.tail())

# Guardar el DataFrame en un archivo CSV
backloggd.to_csv('backloggd.csv')
