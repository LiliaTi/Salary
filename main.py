import requests
from dotenv import load_dotenv
import os
import operator


def predict_rub_salary(salary_from, salary_to):
    if salary_from is None or salary_from == 0:
        return salary_to * 0.8
    elif salary_to is None or salary_to == 0:
        return salary_from * 1.2
    else:
        return (salary_from + salary_to) / 2


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return 0
    elif vacancy['payment_from'] == 0 and vacancy['payment_to'] == 0:
        return 0
    else:
        return predict_rub_salary(vacancy['payment_from'],
                                  vacancy['payment_to'])


def predict_rub_salary_hh(vacancy):
    for key, value in vacancy.items():
        if key == 'salary':
            if value is None:
                return 0
            elif value['currency'] != 'RUR':
                return 0
            else:
                return predict_rub_salary(value['from'], value['to'])


def average_salary_of_page_sj(url_sj, headers_sj, page, language):
    params = {
        'keywords': f'{language}',
        'town': 4,
        'catalogues': 'Разработка, программирование',
        'page': page,
        'count': 100
    }
    response = requests.get(url_sj, headers=headers_sj, params=params)
    response.raise_for_status()
    vacancies_found = len(response.json()['objects'])
    average_salary = 0
    vacancies_processed = 0
    for vacancy in response.json()['objects']:
        predict = predict_rub_salary_sj(vacancy)
        if predict != 0:
            vacancies_processed += 1
        average_salary += predict
    if vacancies_processed != 0:
        average_salary = average_salary / vacancies_processed
    result = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }
    return result


def average_salary_of_page_hh(url_hh, page, language):
    result = {}
    text = f'программист {language}'
    params = {'text': text, 'area': 1,
              'period': 30, 'page': page, 'per_page': 100}
    response = requests.get(url_hh, params=params)
    response.raise_for_status()
    vacancies_found = response.json()['found']
    average_salary = 0
    vacancies_processed = 0
    for vacancy in response.json()['items']:
        predict = predict_rub_salary_hh(vacancy)
        if predict != 0:
            vacancies_processed += 1
        average_salary += predict
    average_salary = average_salary / vacancies_processed
    result = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }
    return result


def hh_results(url_hh, languages):
    results = []
    for language in languages:
        result = {}
        vacancies_processed = 0
        average_salary = 0
        found_pages = 0
        for page in range(0, 20):
            try:
                page_result = average_salary_of_page_hh(url_hh, page, language)
                vacancies_processed += page_result['vacancies_processed']
                average_salary += page_result['average_salary']
                found_pages += 1
            except:
                break
        average_salary = int(average_salary / found_pages)
        result = {
            'language': language,
            'vacancies_found': page_result['vacancies_found'],
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }
        results.append(result)
    sorted_results = sorted(results,
                            key=operator.itemgetter('average_salary'),
                            reverse=True)
    return sorted_results


def sj_results(url_sj, headers_sj, languages):
    results = []
    for language in languages:
        result = {}
        vacancies_processed = 0
        average_salary = 0
        found_pages = 0
        for page in range(0, 500):
            try:
                page_result = average_salary_of_page_sj(url_sj, headers_sj,
                                                        page, language)
                vacancies_processed += page_result['vacancies_processed']
                average_salary += page_result['average_salary']
                vacancies_found += page_result['vacancies_found']
                found_pages += 1
            except:
                break
        if found_pages != 0:
            average_salary = average_salary / found_pages
        result = {
            'language': language,
            'vacancies_found': page_result['vacancies_found'],
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary)
        }
        results.append(result)
    sorted_results = sorted(results,
                            key=operator.itemgetter('average_salary'),
                            reverse=True)
    return sorted_results


def pretty_table(sorted_results, name):
    print()
    print(name)
    print('-' * 90)
    print('|{: <25}|{: <20}|{: <20}|{: <20}|'.format('Язык программирования',
                                                     'Средняя зарплата',
                                                     'Найдено вакансий',
                                                     'Обработано вакансий'))
    print('-' * 90)
    for result in sorted_results:
        print('|{: <25}|{: >20}|{: >20}|{: >20}|'.format(result['language'],
                                                         result['average_salary'],
                                                         result['vacancies_found'],
                                                         result['vacancies_processed']))
    print('-' * 90)


def main():
    load_dotenv()
    superjob_secret_key = os.getenv('SUPERJOB_SECRET_KEY')
    url_sj = 'https://api.superjob.ru/2.33/vacancies'
    url_hh = 'https://api.hh.ru/vacancies'
    headers_sj = {'X-Api-App-Id': superjob_secret_key}
    popular_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'TypeScript',
        'Go'
    ]

    pretty_table(hh_results(url_hh, popular_languages), 'HeadHunter-Moscow')
    print()
    pretty_table(sj_results(url_sj, headers_sj, popular_languages),
                 'SuperJob-Moscow')


if __name__ == '__main__':
    main()
