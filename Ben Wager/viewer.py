from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

comments = json.loads(open("template.json", "r").read())["comments"]

for comment in comments:
	print(comment)
	browser = webdriver.Chrome("../Utilities/chromedriver.exe")
	