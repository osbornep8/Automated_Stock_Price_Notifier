import os
import yagmail
from selenium import webdriver
from selenium.webdriver.common.by import By
import time



def get_driver(url):
    # create an MS Edge driver to access the link and scrape the site
    options = webdriver.EdgeOptions()
    # Set options to make browsing easier
    options.add_argument('disable-infobars')
    options.add_argument('--headless')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('disable-blink-features=AutomationControlled')

    driver = webdriver.Edge(options)
    driver.get(url)
    return driver


def extract_txt(text):
    txt = text.split(' ')[0]
    return float(txt)


def send_mail(to_user, current_val):
    from_user = os.getenv('email')
    password = os.getenv('password')
    subject = f"Stock Price Change @{time.strftime('%a, %I:%M:%S %p %d/%M/%Y')}"
    content = f'''
    Hi {to_user.split('@')[0]},
    As per your notification, a change in the stock price was detected.
    The % change is now: {current_val}%
    Regards,
    Automated Stock Price Notifier
    '''

    yag = yagmail.SMTP(user=from_user, password=password)
    yag.send(to=to_user, subject=subject, contents=content)


def main():
    driver = get_driver('https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6')
    time.sleep(3)
    stock_price = driver.find_element(By.CSS_SELECTOR,
                                      value='#app_indeks > section.page-heading > div > div > div.stock-page-center > span.stock-trend.trend-drop').text
    current_price = extract_txt(stock_price)
    if current_price < (-0.10):
        send_mail(to_user='affdgdaet@yomail.info', current_val=current_price)


main()
