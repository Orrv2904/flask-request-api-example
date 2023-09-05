import os
from flask import Flask, request, render_template
import requests
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('search.html')

@app.route('/album', methods=['POST'])
def album():
    artista = request.form['artista']

    # Realiza la solicitud a la API de Spotify
    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q": artista, "type": "multi", "offset": "0", "limit": "10", "numberOfTopResults": "5"}
    headers = {
        "X-RapidAPI-Key": "dd03069afbmsh67292d8018889fep197c7djsn3f98e606e1a2",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Imprime la respuesta completa de la API en la consola para depurar
    print(json.dumps(data, indent=4))

    # Extrae los nombres de los álbumes y las imágenes de portada
    albums = []
    for item in data.get('albums', {}).get('items', []):
        album_name = item.get('data', {}).get('name', '')
        cover_url = item.get('data', {}).get('coverArt', {}).get('sources', [{}])[0].get('url', '')
        albums.append({'name': album_name, 'cover_url': cover_url})

    # Renderiza una plantilla HTML para mostrar los álbumes
    return render_template('albums.html', artist=artista, albums=albums)




if __name__ == '__main__':
    app.run()