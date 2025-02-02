from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup
import io
import logging
import PyPDF2
import ast
from anytree import Node
from googlesearch import search
from firecrawl import FirecrawlApp

from scrape import crawl
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from random import randint
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Claude:
    def __init__(self):
        self.socketio = socketio
        self.anthropic = Anthropic(
            api_key="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"
        )
        self.crawl = crawl()

    def url_to_info_pls(self, url):
        print(url)
        return self.crawl.crawl_url(url)

    def url_to_info(self, url):
        try:
            response = requests.get(url)
            #print(url, response.status_code)
        except:
            return None
        
        if response.status_code != 200:
            return None

        content_type = response.headers.get("Content-Type", "").lower()
        if "pdf" in content_type:
            # Process PDF content
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            for element in soup(["script", "style"]):
                element.decompose()
            return soup.get_text(separator=" ", strip=True)

    def claude_summarize(self, text):
        message = self.anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            temperature=0,
            system="""
                Summarize the text emphasizing clues of its historical and causal antecedents to aid in discovering prior related articles, papers, or posts.
                Write this analysis explicity then a delimiter then formulate 3 hypotheses of search queries that should yield relevant predecessors
                in the format: analysis !!! [hypothesis1, hypothesis2, hypothesis3] do not put anything after the closing square bracket
            """,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        )

        text = message.content[0].text
        summary, hypotheses = text.split("!!!")
        hypotheses = ast.literal_eval(hypotheses.strip())
        return summary, hypotheses
    
    def claude_closeness(self, summary, proposal):
        message = self.anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            temperature=0,
            system="""You will be given two texts. The first text is a summary of an idea, while the second is a proposed text to be evaluated as its potential causal predecessor. Your task is to assess whether the proposed text can be seen as a causal predecessor of the idea summarized. Provide a clear reasoning explanation for your evaluation. At the very end of your response, output a two-digit similarity rating (00 to 99) with no additional text following it.""",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Summary:\n{summary}\nProposed text:\n{proposal[:1000]}"
                        }
                    ]
                }
            ]
        )

        text = message.content[0].text
        rating = int(text[-2:])
        return rating

    def search_results(self, hypothesis, max_results=5):
    # Perform a Google search and get the top 5 results
        search_results = []
        for url in search(hypothesis, num_results=20):
            
            if len(search_results) == max_results:
                break
            # Check if the URL is like an article
            if any(keyword in url for keyword in ['article', 'news', 'blog', 'post']):
                search_results.append(url)
        return search_results
    
    def recurse(self, parent, url, depth, max_depth=3):
        if depth >= max_depth:
            return

        text = self.url_to_info(url)
        if text is None:
            return
        summary, hypotheses = self.claude_summarize(text[:2000])
        results = []
        for hypothesis in hypotheses:
            search_results = self.search_results(hypothesis, max_results=2)
            for url in search_results:
                info = self.url_to_info(url)
                if info is None:
                    continue
                #rating = self.claude_closeness(summary, info)
                #dictionary[url] = rating
                results.append((url, info))
                if len(results) == 3:
                    break

        top3 = results
        #top3 = sorted(dictionary.items(), key=lambda item: item[1])[::-1][:3]

        for i in range(0, randint(1, 3)):
            self.recurse(Node(top3[i], parent=parent), top3[i][0], depth+1)


    def main(self, url):
        root = Node(url)

        self.recurse(root, url, 0)
        
        return root

    def link_articles(self, param, articles):
        pass