
from dotenv import load_dotenv
import os
import hh_functions
import sj_functions
from common_functions import draw_pretty_table


AMOUNT_OF_PAGES = 100


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

    draw_pretty_table(hh_functions.get_results_hh(url_hh,
                                                  popular_languages,
                                                  AMOUNT_OF_PAGES),
                      'HeadHunter-Moscow')
    print()
    draw_pretty_table(sj_functions.get_results_sj(url_sj,
                                                  headers_sj,
                                                  popular_languages,
                                                  AMOUNT_OF_PAGES),
                      'SuperJob-Moscow')


if __name__ == '__main__':
    main()
