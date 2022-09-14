import os
import json

import requests
import requests.exceptions as r_e
from dotenv import load_dotenv


def check_bitlink(token: str, link: str) -> bool:
    link = remove_protocol_from_bitlink(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(link)
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, headers=headers)
    return response.ok

def check_link(link: str):
    response = requests.get(link)
    response.raise_for_status()

def remove_protocol_from_bitlink(link: str) -> str:
    if link.startswith("https://"):
        link = link[8:]
    elif link.startswith("http://"):
        link = link[7:]
    return link

def shorten_link(token: str, link: str) -> str:
    check_link(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": "Bearer {}".format(token)}
    body = json.dumps({"long_url": link})
    response = requests.post(url=url, data=body, headers=headers)
    response.raise_for_status()
    short_link = response.json()["link"][8:]
    return f"Битлинк: {short_link}"

def count_clicks(token: str, link: str) -> str:
    link = remove_protocol_from_bitlink(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(link)
    params = {"unit": "month", "units": -1}
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    links_number = response.json()["total_clicks"]
    return f"По вашей ссылке прошли {links_number} раз(а)"

def main():
    try:
        load_dotenv()
        token = os.environ["TOKEN"]
        user_input = input("Введите ссылку: ")
        if check_bitlink(token, user_input):
            clicks_count = count_clicks(token, user_input)
            return clicks_count
        else:
            short_link = shorten_link(token, user_input)
            return short_link
    except (r_e.HTTPError, r_e.ConnectionError, r_e.MissingSchema):
        raise TypeError("Нерабочая ссылка")
    except KeyError:
        raise KeyError("Не найден TOKEN в переменных окружения")

if __name__ == "__main__":
    print(main())
