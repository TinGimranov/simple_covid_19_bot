import requests
import smtplib
from lxml import html
from config import login, password, url, smtp_server, smtp_port
from email.mime.text import MIMEText


def send_mail(data_for_mail):
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(login, password)
        msg = MIMEText(
            f"Всего случаев: {data_for_mail['total_cases']}\n"
            f"Новых случаев: {data_for_mail['new_cases']}\n"
            f"Всего смертей: {data_for_mail['total_deaths']}\n"
            f"Динамика смертей: {data_for_mail['new_deaths']}\n"
            f"Всего вылечившихся: {data_for_mail['total_recovered']}\n"
        )
        msg['Subject'] = 'Новая статистика по COVID-19'
        msg['From'] = 'Coronavirus Stat <gimranov.valentin@yandex.ru>'
        msg['To'] = 'gimranov.valentin@yandex.ru'
        server.sendmail('gimranov.valentin@yandex.ru', 'gimranov.valentin@yandex.ru', msg.as_string())


def get_data(country):
    response = requests.get(url)
    response = response.content.decode('utf-8')
    tree = html.fromstring(response)
    table = tree.get_element_by_id("main_table_countries_today")
    country_element = table.xpath(f".//a[contains(text(), '{country}')]")[0]
    row = country_element.xpath('./../..')[0]
    data = row.text_content().split('\n')
    result = {
        'total_cases': data[2],
        'new_cases': data[3],
        'total_deaths': data[4],
        'new_deaths': data[5],
        'total_recovered': data[6],
    }
    return result
