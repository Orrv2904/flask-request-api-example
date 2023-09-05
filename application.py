import os
from flask import Flask, request, render_template
import requests
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

api_key = os.environ.get("X_RapidAPI_Key")
api_host = os.environ.get("X_RapidAPI_Host")

if api_key is None or api_host is None:
    raise Exception("Debes configurar las variables de entorno X_RapidAPI_Key y X_RapidAPI_Host.")

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/album', methods=['POST'])
def album():
    artista = request.form['artista']

    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q": artista, "type": "multi", "offset": "0", "limit": "10", "numberOfTopResults": "5"}
    headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": api_host
    }   
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(json.dumps(data, indent=4))
    albums = []
    for item in data.get('albums', {}).get('items', []):
        album_name = item.get('data', {}).get('name', '')
        cover_url = item.get('data', {}).get('coverArt', {}).get('sources', [{}])[0].get('url', '')
        albums.append({'name': album_name, 'cover_url': cover_url})

    return render_template('albums.html', artist=artista, albums=albums)

if __name__ == '__main__':
    app.run()