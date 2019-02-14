
from textblob import TextBlob, Word, Blobber
import webbrowser
import requests
from bs4 import BeautifulSoup


def get_page(url):
	
	response = requests.get(url)
	page = str(BeautifulSoup(response.content, 'lxml'))
	return page

def get_next_url(page):

	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1: end_quote]
	return url, end_quote
	
def get_all_urls(page):
	
	links = []
	while True:
		url, end_pos = get_next_url(page)
		if url:
			links.append(url)
			page = page[end_pos:]
		else:
			break
	return links
	
def union(links, page):

	for link in page:
		if link not in links:
			links.append(link)
	
def crawl_web(seed_page):
	
	to_crawl = [seed_page]
	crawled = []
	while to_crawl:
		while True:
			page = to_crawl.pop()
			if(page[0:4] == 'http'):
				break
		if page not in crawled:
			pag = get_page(page)
			links = get_all_urls(pag)
			union(to_crawl, links)
			crawled.append(page)
			for i in crawled:
				print (i)
		else:
			continue
	return crawled

def main():
	crawled = crawl_web('https://xkcd.com/')
	for page in crawled:
		print (page)

if __name__ == '__main__':
    main()