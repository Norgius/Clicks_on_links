import os
from urllib.parse import urlparse

import requests
import requests.exceptions as r_e
from dotenv import load_dotenv


def is_bitlink(token: str, link: str) -> bool:
    link = remove_protocol_from_bitlink(link)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(link)
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, headers=headers)
    return response.ok


def remove_protocol_from_bitlink(link: str) -> str:
    parsed_link = urlparse(link)
    return f"{parsed_link.netloc}{parsed_link.path}"


def shorten_link(token: str, link: str) -> str:
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": "Bearer {}".format(token)}
    body = {"long_url": link}
    response = requests.post(url=url, json=body, headers=headers)
    response.raise_for_status()
    bitlink = response.json().get("id")
    return bitlink


def count_clicks(token: str, link: str) -> str:
    link = remove_protocol_from_bitlink(link)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary"
    params = {"unit": "month", "units": -1}
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    clicks_number = response.json().get("total_clicks")
    return clicks_number


def main():
    try:
        load_dotenv()
        token = os.environ["BITLY_TOKEN"]
        user_input = input("Введите ссылку: ")
        if is_bitlink(token, user_input):
            clicks_count = count_clicks(token, user_input)
            formed_response = f"По вашей ссылке прошли {clicks_count} раз(а)"
        else:
            short_link = shorten_link(token, user_input)
            formed_response = f"Битлинк: {short_link}"
        return formed_response
    except (r_e.HTTPError, r_e.ConnectionError, r_e.MissingSchema):
        raise TypeError("Нерабочая ссылка")
    except KeyError:
        raise KeyError("Не найден BITLY_TOKEN в переменных окружения")


if __name__ == "__main__":
    print(main())
