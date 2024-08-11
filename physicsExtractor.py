import requests
from bs4 import BeautifulSoup
import re
import uuid
from datetime import datetime
import json

def extract_questions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    questions = re.split(r'\d+\.\s', content)[1:]

    extracted_questions = []
    for question in questions:
        question_id = str(uuid.uuid4())
        question_match = re.search(r'(.*?)(?=\(A\))', question, re.DOTALL)
        if question_match:
            question_text = question_match.group(1).strip()
        else:
            continue
        options_start = re.search(r'\(A\)', question)
        question_html = soup.find(string=re.compile(re.escape(question_text)))

        image_urls = []
        if question_html and question_html.parent:
            current_element = question_html.parent.next_sibling
            while current_element and (options_start is None or current_element != options_start):
                if current_element.name == 'img':
                    image_urls.append(current_element['src'])
                current_element = current_element.next_sibling

        options = []
        options_matches = re.findall(r'\((A|B|C|D)\)\s(.*?)\n', question)
        for label, text in options_matches:
            options.append({"label": label, "text": text.strip()})

        correct_label_match = re.search(r'Answer\s\((A|B|C|D)\)', question)
        correct_label = correct_label_match.group(1).strip() if correct_label_match else ""

        question_data = {
            "id": question_id,
            "metadata": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "website": "byjus.com",
                "exam": "JEE Main 2022",
                "url": url,
            },
            "content": {
                "is_multimodal": 1 if image_urls else 0,
                "question": question_text,
                "options": options,
                "images": image_urls,
                "correct_label": correct_label
            }
        }

        extracted_questions.append(question_data)

    return extracted_questions

def extract_multiple_links(urls):
    all_extracted_data = []

    for url in urls:
        extracted_data = extract_questions(url)
        all_extracted_data.extend(extracted_data)

    return all_extracted_data

# List of URLs
urls = [
    "https://byjus.com/jee/jee-main-2022-question-paper-physics-july-25-shift-1/",
    "https://byjus.com/jee/jee-main-2022-question-paper-physics-july-25-shift-2/",
    "https://byjus.com/jee/jee-main-2022-question-paper-physics-july-26-shift-1/"
]


extracted_data = extract_multiple_links(urls)


with open('results.json', 'w') as json_file:
    json.dump(extracted_data, json_file, indent=4)

print("Data has been saved to results.json")