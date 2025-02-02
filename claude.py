from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup
import io
import PyPDF2
import ast


class Claude:
    def __init__(self):
        self.anthropic = Anthropic(
            api_key="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"
        )

    def url_to_info(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error fetching URL: {response.status_code}")

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
            max_tokens=1000,
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
        hypotheses = text.split("!!!")[1].strip()
        hypotheses = ast.literal_eval(hypotheses)
        return hypotheses
    



c = Claude()
text = c.url_to_info("https://arxiv.org/pdf/1706.03762")
print(c.claude_summarize(text[:10000]))