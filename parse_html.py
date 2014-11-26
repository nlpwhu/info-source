from bs4 import BeautifulSoup
import requests

def parse(url):
	response  = requests.get(url).content
	return response