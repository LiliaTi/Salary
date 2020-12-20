from common_functions import predict_rub_salary
import requests
import operator


def predict_rub_salary_hh(vacancy):
    for key, value in vacancy.items():
        if key == 'salary':
            if not value or value['currency'] != 'RUR':
                return 0
            else:
                return predict_rub_salary(value['from'], value['to'])


def get_info_of_page_hh(url_hh, page, language):
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


def get_results_hh(url_hh, languages, amount_of_pages):
    results = []
    for language in languages:
        result = {}
        vacancies_processed = 0
        average_salary = 0
        found_pages = 0
        for page in range(0, amount_of_pages):
            try:
                page_result = get_info_of_page_hh(url_hh, page, language)
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
