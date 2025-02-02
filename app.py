from flask import Flask, render_template, request, jsonify
import requests
from googlesearch import search

app = Flask(__name__)

def mock_search(query):
    # Perform a Google search and get the top 5 results
    search_results = []
    for url in search(query, num_results=20):
        if len(search_results) == 5:
            break

        else:
            search_results.append({
                'title': url,  # Mock title based on the query
                'url': url,
                'sources': ['Google']
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

if __name__ == '__main__':
    app.run(debug=True)