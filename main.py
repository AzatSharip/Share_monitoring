# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import smtplib  # Импортируем библиотеку по работе с SMTP
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
import time
import datetime
import sys
import os



def price_checker(url):
    ''' Парсим сайт yahoo.finance с задержкой и берем стоимость акции в реальном времени'''
    time.sleep(60)
    r = requests.get(url)
    #print(r.status_code)
    soup = BeautifulSoup(r.text, features="html.parser")
    pars_price = soup.find_all("div", {"class": "My(6px) Pos(r) smartphone_Mt(6px)"})[0].find_all(text=True, recursive=True)
    price = float(pars_price[0].replace(',', ''))
    market_status = pars_price[2]
    print(price)
    return price, market_status

def email_sender(message):
    addr_from = "matvei.elagin87@gmail.com"  # Адресат
    addr_to = "azat.sharip@gmail.com"  # Получатель
    password = "matveielagin16071987"  # Пароль

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'Atention! Message from "Share-monitoring" script!'  # Тема сообщения

    body = message
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()



def market_status_checker():
    #print(datetime.date.today())
    current_time = int(datetime.datetime.today().strftime("%H"))
    if current_time >= 12 and current_time < 21:
        return True
    else:
        return False


def close_counter(value):
    time.sleep(1)
    for i in range(value + 1):
        # os.system('CLS')
        print(f'----------------- {value - i} -----------------')
        time.sleep(1)
    sys.exit()


def main():
    url = 'https://finance.yahoo.com/quote/LKOH.ME?p=LKOH.ME&.tsrc=fin-srch'
    print('Price Controller launched!')
    while True:
        while market_status_checker() == True:
            price, market_status = price_checker(url)

            if price >= 5200:
                email_sender(f'Price = {price}')
                print(f'Attention! Price is {price}!')
                close_counter(10)
        else:
            print('Market is closed!')
            time.sleep(300)


if __name__ == '__main__':
    main()


