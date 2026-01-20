import requests
from bs4 import BeautifulSoup

URL = "http://swgoh.gg/"
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.find('div'))