from flask import Flask, render_template, request, jsonify
import requests
from flask_socketio import SocketIO
from googlesearch import search
from functools import lru_cache
from claude import Claude
import threading
from queue import Queue

def run_claude(socketio, url, queue):
    c = Claude(socketio)
    root, output = c.main(url)
    queue.put((root, output))

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
    queue = Queue()
    thread = threading.Thread(target=run_claude, args=(socketio, url, queue))
    thread.start()
    thread.join()  # Wait for the thread to finish
    root, output = queue.get()  # Get the result from the queue
    return render_template("click/index.html", url=url)


