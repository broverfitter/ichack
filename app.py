from flask import Flask, render_template, request, jsonify
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from claude import Claude  # Import the Claude class

def get_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            return description.get('content')
        else:
            return 'No description available'
    except requests.exceptions.RequestException as e:
        return f'Error fetching the URL: {e}'

def recursive_search(query, depth, max_depth=3):
    if depth > max_depth:
        return []

    results = mock_search(query)
    all_articles = []

    for result in results:
        url = result['url']
        claude = Claude()
        text = claude.url_to_info(url)
        hypotheses = claude.claude_summarize(text[:10000])

        all_articles.append(text[:10000])

        for hypothesis in hypotheses:
            all_articles.extend(recursive_search(hypothesis, depth + 1, max_depth))

    return all_articles

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
    for url in search(query, num_results=50):
        if len(search_results) == 5:
            break
        # Check if the URL is like an article
        if any(keyword in url for keyword in ['article', 'news', 'blog', 'post']):
            search_results.append({
                'title': f'Article about {get_description(url)}',  # Mock title based on the query
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

@app.route('/claude', methods=['POST'])
def claude_view():
    data = request.get_json()
    url = data.get('url')
    claude = Claude()
    original_text = claude.url_to_info(url)
    articles = recursive_search(url, 1)
    linked_summary = claude.link_articles(original_text[:10000], articles)
    return jsonify({'summary': linked_summary})

if __name__ == '__main__':
    app.run(debug=True)