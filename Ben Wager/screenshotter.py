from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
from time import sleep
from html import unescape


def makeFolder(id):
    try:
        os.makedirs('Screenshots/' + id + '/')
    except FileExistsError:
        pass


if not os.path.isdir('Outputs'):
    os.mkdir('Outputs')


def takeScreenshots(id):
    browser = webdriver.Chrome('../Utilities/chromedriver.exe')
    browser.maximize_window()

    makeFolder(id)
    
    fullFile = json.loads(open('Outputs/' + id + '.json', 'r').read())
    comments = fullFile['comments']

    fullFile['title'] = unescape(fullFile['title'])
    fullFile['title'] = fullFile['title'].replace("'", "\\'")
    fullFile['title'] = fullFile['title'].replace('\n', '\\n')

    browser.get(os.getcwd() + '\\HTML\\title.html')
    browser.execute_script("document.querySelector('#title-author').innerText = '"
                            + fullFile['author'] + "'")
    browser.execute_script("document.querySelector('#score').innerText = '"
                            + fullFile['score'] + " points'")
    browser.execute_script("document.querySelector('#title').innerText = '"
                            + fullFile['title'] + "'")
    makeFolder(fullFile['id'])
    browser.save_screenshot('Screenshots/' + fullFile['id']
                            + '/Title.png')

    for comment in comments:
        comment['comment'] = unescape(comment['comment'])
        comment['comment'] = comment['comment'].replace("'", "\\'")
        comment['comment'] = comment['comment'].replace('\n', '\\n')

        browser.get(os.getcwd() + '\\HTML\\comment.html')
        browser.execute_script("document.querySelector('#author').innerText = '"
                                + comment['author'] + "'")
        browser.execute_script("document.querySelector('#score').innerText = '"
                                + comment['score'] + " points'")
        browser.execute_script("document.querySelector('#created').innerText = '"
                                + comment['created'] + " ago'")
        browser.execute_script("document.querySelector('#comment').innerText = '"
                                + comment['comment'] + "'")
        browser.save_screenshot('Screenshots/' + fullFile['id'] + '/'
                                + comment['id'] + '.png')
    browser.quit()
