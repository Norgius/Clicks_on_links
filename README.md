# Считаем клики по ссылкам
Данная программа позволяет создавать `bit.ly ссылки` и считать количество переходов по данным `bit.ly ссылкам`.

Для запуска установите виртуальное окружение и библиотеки из файла `requirements.txt`.
```
$ python3.10 -m venv env

$ . ./env/bin/activate

$ pip install -r requirements.txt
```
Для работы с bit.ly ссылками потребуется токен, чтобы его получить, нужно зарегистрироваться на сайте https://app.bitly.com/.

После регистрации токен можно получить по ссылке https://app.bitly.com/settings/api/. Для безопасности создайте скрытый файл `.env`. Впишите токен в только что созданный файл под ключом `BITLY_TOKEN=`

Запустим саму программу.
```
$ python main.py
```