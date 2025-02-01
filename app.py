# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    sample_article = {
        'title': 'DeepSeekMath: Pushing the Limits of Math...',
        'url': 'https://arxiv/whatever',
        'sources': ['Source 1', 'Source 2', 'Source 3']
    }
    return render_template('index.html', article=sample_article)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    # This is where you'll implement the actual search logic later
    # For now, just return a sample response
    response = {
        'title': f'Results for: {query}',
        'url': query,
        'sources': ['Found Source 1', 'Found Source 2', 'Found Source 3']
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)