// static/script.js
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent the default form submission
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
        // Clear previous results
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = '';

        // Display top 5 results
        data.results.forEach(result => {
            const articleContainer = document.createElement('div');
            articleContainer.className = 'article-container';

            const articleContent = `
                <div class="article-content">
                    <h2>${result.title}</h2>
                    <p class="article-url">${result.url}</p>
                </div>
                <div class="sources">
                    ${result.sources.map(source => `<button class="source-button">${source}</button>`).join('')}
                </div>
            `;
            articleContainer.innerHTML = articleContent;
            resultsContainer.appendChild(articleContainer);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}