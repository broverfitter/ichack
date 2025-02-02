from firecrawl import FirecrawlApp

class crawl:
    def __init__(self):
        self.app = FirecrawlApp(api_key="fc-827d769bc5c14316871971dd813607f3")

    def crawl_url(self, url):
        crawl_status = self.app.crawl_url(
            url,
            params={
                'limit': 100,
                'scrapeOptions': {'formats': ['markdown', 'html']}
            },
            poll_interval=30
        )
        return crawl_status['data'][0]['html']