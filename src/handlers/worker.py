from bs4 import BeautifulSoup
import requests

questions_url = 'https://rosstat.gov.ru/folder/165737'
news_url = 'https://71.rosstat.gov.ru/news'


def get_news(i):

    page = requests.get(news_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    all_news = soup.find_all('div', class_='news-card')
    news_titles = []
    news_data = []
    news_content = []

    for elem in all_news:
        title_tag = elem.find('div', class_='news-card__title')
        href_tag = title_tag.find('a')
        news_titles.append(href_tag.text)
        news_data.append(elem.find('div', class_='news-card__data').text)

        news_page = requests.get(href_tag['href'])
        news_soup = BeautifulSoup(news_page.text, 'html.parser')
        content = news_soup.find('div', class_='content')
        paragraphs = content.find_all('p')

        news_str = ''
        for p in paragraphs:
            news_str += p.text + '\n'
        news_content.append(news_str)
    
    mess_str = news_titles[i] + '\n\n' + news_content[i] + '\n\n' + news_data[i]

    return mess_str


def get_questions():

    page = requests.get(questions_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    all_questions = soup.find_all('div', class_='toggle-card__title')
    questions = []
    for elem in all_questions:
        questions.append(elem.text)

    return questions


def get_answers():

    page = requests.get(questions_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    all_answers = soup.find_all('div', class_='toggle-card__main-content')
    filtered_answers = []
    i = 0
    for elem in all_answers:
        answer = elem.find_all('p')
        filtered_answers.append('')
        for e in answer:
            filtered_answers[i] += e.text + '\n'
        i += 1

    return filtered_answers