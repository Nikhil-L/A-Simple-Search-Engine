
from textblob import TextBlob, Word, Blobber
import webbrowser
import requests
from bs4 import BeautifulSoup


def get_page(url):
	
	response = requests.get(url)
	page = str(BeautifulSoup(response.content, 'lxml'))
	return page

def clean(content):
	content = TextBlob(content)
	return content.words
	
def crawl_web(seed_page):
	
	to_crawl = [seed_page]
	crawled = []
	next_depth = []
	index = {}
	num = 0
	while to_crawl and num <= 1:
		while to_crawl:
			page = to_crawl.pop()
			if(page[0:4] == 'http'):
				num = num + 1
				break
		if page not in crawled:
			content = get_page(page)
			soup = BeautifulSoup(content, 'lxml')
			txt = soup.get_text()
			add_page_to_index(index, page, txt)
			links = get_all_links(content)
			union(to_crawl, links)
			crawled.append(page)
	return crawled, index
	
def get_next_link(page):

	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1: end_quote]
	return url, end_quote
	
def get_all_links(page):
	
	links = []
	while True:
		url, end_pos = get_next_link(page)
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
			
def add_page_to_index(index, url, content):
	
	content = clean(content)
	for word in content:
		if len(word) > 5 and len(word) < 15:
			add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
        
def main():
	crawled, index = crawl_web('https://xkcd.com/')
	for key in index:
		print(key)
	k = raw_input("Enter the keyword you are searching for : ")
	urls = lookup(index, k)
	if urls:
		for url in urls:
			print(url)

if __name__ == '__main__':
    main()