import requests
from bs4 import BeautifulSoup
import json
import uuid
from datetime import datetime
import re

def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_correct_label(answer_text):
    match = re.search(r'Answer *\( *([A-D]) *\)', answer_text)
    if match:
        return match.group(1)
    return None

def parse_options(options):
    formatted_options = []
    for opt in options:
        if opt:  # Ensure the option is not empty
            match = re.match(r'\((A|B|C|D)\) (.*)', opt)
            if match:
                label = match.group(1)
                text = match.group(2)
                formatted_options.append({
                    "label": label,
                    "text": text
                })
    return formatted_options

def parse_questions(html):
    soup = BeautifulSoup(html, 'html.parser')
    questions = soup.find_all('div', class_='questions')
    
    extracted_data = []
    
    for question_div in questions:
        try:
            question_title = question_div.find('span', class_='question-title').text.strip()
            sub_question = question_div.find('span', class_='sub-question')
            if sub_question is None:
                continue
            options = [opt.text.strip() for opt in sub_question.find_all('p')]
            sub_answer = question_div.find('span', class_='sub-answer')
            if sub_answer and sub_answer.find('strong'):
                answer = sub_answer.find('strong').text.strip()
                correct_label = extract_correct_label(answer)
            else:
                correct_label = None
            
            # Collect images that are not inside sub_answer
            images = []
            for img in question_div.find_all('img'):
                if sub_answer and img in sub_answer.find_all('img'):
                    continue
                images.append(img['src'])

            is_multimodal = 1 if images else 0
            image_srcs = images
            
            formatted_options = parse_options(options)

            question_data = {
                "id": str(uuid.uuid4()),
                "metadata": {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "website": "example.com",
                    "exam": "Sample Exam",
                    "url": url
                },
                "content": {
                    "is_multimodal": is_multimodal,
                    "question": question_title,
                    "options": formatted_options,
                    "images": image_srcs,
                    "correct_label": correct_label
                }
            }
            
            extracted_data.append(question_data)
        except Exception as e:
            print(f"Error processing question: {e}")
    
    return extracted_data

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


url = "https://byjus.com/jee/jee-main-2022-question-paper-maths-june-24-shift-1/"
html_content = fetch_webpage(url)
questions_data = parse_questions(html_content)
json_path = "maths.json"
save_to_json(questions_data, json_path)

print(f"Data saved to {json_path}")