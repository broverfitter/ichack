from flask import Flask, render_template, request, jsonify
from googlesearch import search

app = Flask(__name__)

@app.route('/')
def home():
    sample_article = {
        'title': 'DeepSeekMath: Pushing the Limits of Math...',
        'url': 'https://arxiv/whatever',
        'sources': ['Source 1', 'Source 2', 'Source 3']
    }
    return render_template('index.html', article=sample_article)

def mock_search(query):
    # Perform a Google search and get the top 5 results
    search_results = []
    for url in search(query, num_results= 50):
        if len(search_results) == 5:
            break
        # Check if the URL is like an article
        if any(keyword in url for keyword in ['article', 'news', 'blog', 'post']):
            search_results.append({
                'title': f'Article about {query}',  # Mock title based on the query
                'url': url,
                'sources': ['Google']
            })
    return search_results

@app.route('/search', methods=['POST'])
def search_view():
    data = request.get_json()
    query = data.get('query')
    results = mock_search(query)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)