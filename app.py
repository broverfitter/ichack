from flask import Flask, render_template, request, jsonify
import requests
from flask_socketio import SocketIO
from googlesearch import search
from functools import lru_cache
from claude import Claude
import threading

def run_claude(socketio, url):
    c = Claude(socketio)
    root,output = c.main(url)




app = Flask(__name__)
socketio = SocketIO(app)

def mock_search(query):
    search_results = []
    for url in search(query, num_results=20):
        if len(search_results) == 5:
            break
        else:
            search_results.append({
                'url': url,
            })
    return search_results

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search_view():
    data = request.get_json()
    query = data.get('query')
    results = mock_search(query)
    print(results)
    return jsonify({'results': results})

@app.route('/click')
def click_view():
    url = request.args.get('url')
    threading.Thread(target=run_claude, args=(socketio, url)).start()
    return render_template("click/index.html", url=url)


