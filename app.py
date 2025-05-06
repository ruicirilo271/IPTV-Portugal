from flask import Flask, render_template, request
import requests

app = Flask(__name__)

M3U8_URL = "https://raw.githubusercontent.com/LITUATUI/M3UPT/refs/heads/main/M3U/M3UPT.m3u"

def parse_m3u8(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    canais = []
    nome = None
    for line in lines:
        if line.startswith('#EXTINF:'):
            nome = line.split(',')[-1].strip()
        elif line.startswith('http'):
            canais.append({'nome': nome, 'url': line.strip()})
    return canais

@app.route('/', methods=['GET', 'POST'])
def index():
    canais = parse_m3u8(M3U8_URL)
    selected_url = None
    if request.method == 'POST':
        selected_url = request.form.get('canal')
    return render_template('index.html', canais=canais, selected_url=selected_url)

if __name__ == '__main__':
    app.run(debug=True)
