

from textblob import TextBlob, Word, Blobber
import webbrowser
import requests
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def get_page(url):
	
	response = requests.get(url)
	page = response.text
	return page

def clean(content):
	content = TextBlob(content)
	ps = PorterStemmer()
	i = 0
	contents = content.words
	for word in contents:
		contents[i] = ps.stem(word)
		i = i + 1
	return contents
	
def crawl_web(seed_page):

	to_crawl = [seed_page]
	crawled = []
	next_depth = []
	index = {}
	num = 0
	while to_crawl and num <= 3:
		page = to_crawl.pop()
		num = num + 1
		if(len(to_crawl) > 100):
			break
		if page not in crawled:
			content = get_page(page)
			soup = BeautifulSoup(content, 'lxml')
			txt = soup.get_text()
			add_page_to_index(index, page, txt)
			links = get_all_links(soup)
			union(to_crawl, links)
			crawled.append(page)
	return crawled, index
	
	
def get_all_links(page):
	
	links = []
	tags = page.find_all('a')

	for tag in tags:
		url = tag.get('href')
		if url:
			if url[0:4] == "http":
				links.append(url)
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

def open_browser(url):
	webbrowser.open(url)

def main():
	crawled, index = crawl_web('https://xkcd.com/')
	#for key in index:
		#print(key)
	ps = PorterStemmer()
	k = raw_input("Enter the keyword you are searching for : ")
	k = ps.stem(k)
	urls = lookup(index, k)
	if urls:
		url = urls[len(urls)/2]
		open_browser(url)
	
	else:
		print("No website found!!")

if __name__ == '__main__':
    main()