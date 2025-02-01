# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Placeholder for actual article data
    sample_article = {
        'title': 'DeepSeekMath: Pushing the Limits of Math...',
        'url': 'https://arxiv/whatever',
        'sources': ['Source 1', 'Source 2', 'Source 3']
    }
    return render_template('index.html', article=sample_article)

if __name__ == '__main__':
    app.run(debug=True)