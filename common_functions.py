def predict_rub_salary(salary_from, salary_to):
    if not salary_from or salary_from == 0:
        return salary_to * 0.8
    elif not salary_to or salary_to == 0:
        return salary_from * 1.2
    else:
        return (salary_from + salary_to) / 2


def draw_pretty_table(sorted_results, name):
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
