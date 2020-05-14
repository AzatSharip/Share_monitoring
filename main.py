# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import smtplib  # Импортируем библиотеку по работе с SMTP
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
import time


def price_checker(url):
    ''' Парсим сайт yahoo.finance с задержкой и берем стоимость акции в реальном времени'''
    time.sleep(1)
    r = requests.get(url)
    #print(r.status_code)
    soup = BeautifulSoup(r.text, features="html.parser")
    pars_price = soup.find_all("div", {"class": "My(6px) Pos(r) smartphone_Mt(6px)"})[0].find_all(text=True, recursive=True)
    price = float(pars_price[0].replace(',', ''))
    market_status = pars_price[2]
    print(price)
    return price, market_status

def email_sender(price):
    addr_from = "matvei.elagin87@gmail.com"  # Адресат
    addr_to = "azat.sharip@gmail.com"  # Получатель
    password = "matveielagin16071987"  # Пароль

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = f'Atention! Price = {price}'  # Тема сообщения

    body = "Sell out immediately!"
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()


if __name__ == '__main__':
    url = 'https://finance.yahoo.com/quote/LKOH.ME?p=LKOH.ME&.tsrc=fin-srch'
    status = True
    while status:
        price, market_status = price_checker(url)
        print(market_status)

        if price >= 5200:
            email_sender(price)
            status = False
