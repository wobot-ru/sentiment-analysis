# -*- coding: utf-8 -*-
import codecs
import winsound
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def find_el(parent, how, what):
    try:
        el = parent.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return el


def start():
    driver = webdriver.Firefox()
    url_infos = [{'url': 'http://otzovik.com/review_{0}.html'.format(n), 'id': str(n)} for n in range(1, 300000)]
    for url_info in url_infos:
        # sleep(randint(1, 2))
        driver.get(url_info['url'])
        if find_el(driver, By.NAME, 'captcha_url'):
            print 'enter capcha, please'
            winsound.Beep(700, 1000)
            sleep(60)
        try:
            parse_review(driver, url_info)
        except:
            pass


def parse_review(driver, url_info):
    container = find_el(driver, By.CSS_SELECTOR, 'div.main_txt')
    if not container: return

    pros = find_el(container, By.CSS_SELECTOR, 'div.pro')
    if pros: pros = pros.text.replace(u'Достоинства:', '').strip()

    cons = find_el(container, By.CSS_SELECTOR, 'div.contra')
    if cons: cons = cons.text.replace(u'Недостатки:', '').strip()

    text = find_el(container, By.CSS_SELECTOR, 'div.description > div[itemprop="description"]')
    if text: text = text.text

    summary = find_el(container, By.CSS_SELECTOR, 'div.description > i.summary')
    if summary: summary = summary.text

    rating = find_el(container, By.CSS_SELECTOR, 'div.description > div.rating > abbr.rating')
    if rating: rating = rating.get_attribute('title')

    save({'pros': pros, 'cons': cons, 'text': text, 'summary': summary, 'rating': rating}, url_info)


def save(item, url_info):
    path = './data/otzovik/reviews/' + item['rating'] + '/'
    rev_id = url_info['id']
    write_file(path + rev_id + '_pros.txt', item['pros'])
    write_file(path + rev_id + '_cons.txt', item['cons'])
    write_file(path + rev_id + '_text.txt', item['text'])
    write_file(path + rev_id + '_summary.txt', item['summary'])


def write_file(filename, text):
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(text)


start()
