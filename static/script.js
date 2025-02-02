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

        // Display top 5 results as buttons
        data.results.forEach(result => {
            const articleButton = document.createElement('button');
            articleButton.className = 'article-button';
            articleButton.innerText = result.title;
            articleButton.addEventListener('click', () => {
                showLoadingMessage(result.url);
                hidePreview();
            });
            articleButton.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                togglePreview(result.url, articleButton);
            });
            resultsContainer.appendChild(articleButton);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function showLoadingMessage(url) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `<p>Processing search for: ${url}</p>`;
}

function togglePreview(url, button) {
    const previewContainer = document.getElementById('previewContainer');
    if (previewContainer.style.display === 'block' && previewContainer.dataset.url === url) {
        previewContainer.style.display = 'none';
        previewContainer.innerHTML = '';
    } else {
        const rect = button.getBoundingClientRect();
        previewContainer.innerHTML = `<iframe src="${url}" frameborder="0" class="preview-iframe"></iframe>`;
        previewContainer.style.display = 'block';
        previewContainer.style.top = `${rect.top + window.scrollY}px`;
        previewContainer.style.left = `${rect.left + window.scrollX - previewContainer.offsetWidth}px`;
        previewContainer.dataset.url = url;
    }
}

function hidePreview() {
    const previewContainer = document.getElementById('previewContainer');
    previewContainer.style.display = 'none';
    previewContainer.innerHTML = '';
}