from common_functions import predict_rub_salary
import requests
import operator


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] != 'rub' or (vacancy['payment_from'] == 0 and vacancy['payment_to'] == 0):
        return 0
    else:
        return predict_rub_salary(vacancy['payment_from'],
                                  vacancy['payment_to'])


def get_info_of_page_sj(url_sj, headers_sj, page, language):
    params = {
        'keywords': language,
        'town': 4,
        'catalogues': 'Разработка, программирование',
        'page': page,
        'count': 100
    }
    response = requests.get(url_sj, headers=headers_sj, params=params)
    response.raise_for_status()
    objects = response.json()['objects']
    vacancies_found = len(objects)
    average_salary = 0
    vacancies_processed = 0
    for vacancy in objects:
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


def get_results_sj(url_sj, headers_sj, languages, amount_of_pages):
    results = []
    for language in languages:
        result = {}
        vacancies_processed = 0
        vacancies_found = 0
        average_salary = 0
        found_pages = 0
        for page in range(0, amount_of_pages):
            try:
                page_result = get_info_of_page_sj(url_sj, headers_sj,
                                                        page, language)
                vacancies_processed += page_result['vacancies_processed']
                average_salary += page_result['average_salary']
                vacancies_found += page_result['vacancies_found']
                found_pages += 1
            except requests.exceptions.HTTPError:
                break
        if found_pages != 0:
            average_salary = average_salary / found_pages
        result = {
            'language': language,
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(average_salary)
        }
        results.append(result)
    sorted_results = sorted(results,
                            key=operator.itemgetter('average_salary'),
                            reverse=True)
    return sorted_results
