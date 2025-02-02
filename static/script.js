document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent the default form submission
        const query = this.value;
        searchArticle(query);
    }
});

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

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
        data.results.forEach((result, index) => {
            const articleButton = document.createElement('div');
            articleButton.className = 'article-button'

            articleButton.innerHTML = `
                <div class="button-text">${result.url}</div>
                <div class="preview-container">
                    <iframe src="${result.url}" 
                            frameborder="0" 
                            class="preview-iframe">
                    </iframe>
                </div>
            `;

            articleButton.addEventListener('mouseenter', (e) => {
                const previewIframe = articleButton.querySelector('.preview-iframe');
                previewIframe.style.display = 'block';
                previewIframe.style.height = '400px'
                e.preventDefault();
            });
            articleButton.addEventListener('mouseleave', () => {
                const previewIframe = articleButton.querySelector('.preview-iframe');
                previewIframe.style.height = '0px';
            });
            articleButton.addEventListener('click', () => {
                showLoadingMessage(result.url);
                hidePreview();
            });
            articleButton.querySelector('.preview-iframe').style.display = 'none';
            resultsContainer.appendChild(articleButton);

            setTimeout(() => {
                articleButton.classList.add('visible');
            }, index * 200);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}