import re
import uuid
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from bench.data.base import BaseData
from bench.data.models import DataItem, Metadata, Content
from urllib.parse import urlparse


class BaseData(BaseData):
    def __init__(self):
        super().__init__()

    def parse(self, url):
        items = []
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.get_text()
        questions = re.split(r"\d+\.\s", content)[1:]

        parsed_url = urlparse(url)
        website = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        exam = parsed_url.path.split('/')[2]

        for question in questions:
            question_id = str(uuid.uuid4())
            question_match = re.search(r"(.*?)(?=\(A\))", question, re.DOTALL)
            if question_match:
                question_text = question_match.group(1).strip()
            else:
                continue
            options_start = re.search(r"\(A\)", question)
            question_html = soup.find(string=re.compile(re.escape(question_text)))

            image_urls = []
            if question_html and question_html.parent:
                current_element = question_html.parent.next_sibling
                while current_element and (
                    options_start is None or current_element != options_start
                ):
                    if current_element.name == "img":
                        image_urls.append(current_element["src"])
                    current_element = current_element.next_sibling

            options = []
            options_matches = re.findall(r"\((A|B|C|D)\)\s(.*?)\n", question)
            for label, text in options_matches:
                options.append({"label": label, "text": text.strip()})

            correct_label_match = re.search(r"Answer\s\((A|B|C|D)\)", question)
            correct_label = (
                correct_label_match.group(1).strip() if correct_label_match else ""
            )

            data = DataItem(
                id=question_id,
                metadata=Metadata(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    website=website,
                    exam=exam,
                    url=url,
                ),
                content=Content(
                    is_multimodal=1 if image_urls else 0,
                    question=question_text,
                    options=options,
                    images=image_urls,
                    correct_label=correct_label,
                ),
            )
            items.append(data)
        return items
