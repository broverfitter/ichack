from flask import Flask, render_template, request, jsonify
import requests
from googlesearch import search
from functools import lru_cache

app = Flask(__name__)

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
    return render_template("click/index.html", url=url)
    

if __name__ == '__main__':
    app.run(debug=True)