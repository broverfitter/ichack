// static/script.js
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const query = this.value;
        searchArticle(query);
    }
});

function searchArticle(query) {
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        // Update the article content
        document.getElementById('articleTitle').textContent = data.title;
        document.getElementById('articleUrl').textContent = data.url;

        // Update the sources
        const sourcesContainer = document.getElementById('sourcesContainer');
        sourcesContainer.innerHTML = '';
        data.sources.forEach(source => {
            const button = document.createElement('button');
            button.className = 'source-button';
            button.textContent = source;
            sourcesContainer.appendChild(button);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}