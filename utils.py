import requests
from settings import BULLYING_ANALYSIS_URL


def get_arg(arg):
    return int(arg.split()[-1])


def check_bullying(text):
    response = requests.post(url=BULLYING_ANALYSIS_URL, data={'text': text})
    print(response.json())
    return response.json()


def get_info_about_bullying(text):
    response = requests.post(url=BULLYING_ANALYSIS_URL, data={'text': text})
    data = response.json()
    bulling_percentage = round(data['probability_bad'] * 100, 2)
    bad_words = [remove_special_characters(word) for word in data['bad_words'].keys()]
    bad_words_in_string = ', '.join(list(bad_words))
    return bulling_percentage, bad_words_in_string


def remove_special_characters(word):
    return ''.join(e for e in word if e.isalnum())
