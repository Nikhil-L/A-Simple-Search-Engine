
#import section
import urllib.request
from urllib.error import HTTPError, URLError
import webbrowser
import requests
from bs4 import BeautifulSoup
#from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def get_page(url):
	#get the page
	response = requests.get(url)
	#convert the page into text format
	page = response.text
	return page

def clean(content):
	#tokenize the text into list of words
	content = word_tokenize(content)
	#remove punctuations and convert to lowercase
	content = [word.lower() for word in content if word.isalpha()]
	stop_words = set(stopwords.words('english'))
	stop_words.add("this")
	#usage of SnowballStemmer to apply stemming for words in list
	#stemmer = SnowballStemmer("english")
	i = 0
	for word in content:
		if(word not in stop_words):
			#stemming the words
			content[i] = word
			i = i + 1
		else:
			# word is a stop words then delete that word
			del content[i]
	return content

def crawl_web(seed_page):
	to_crawl = [seed_page]
	crawled = []
	next_depth = []
	index = {}
	graphs = {}
	num = 0
	#make the loop crawl for the length of 7 pages
	while to_crawl and num <= 10:
		page = to_crawl.pop()
		num = num + 1

		if page not in crawled:
			#get the page
			content = get_page(page)
			#convert the page into parsable format
			soup = BeautifulSoup(content, 'lxml')
			#get text from the soup
			headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
			txt = str([header.get_text() for header in headers])
			#adds the all the keywords in the page to the index
			add_page_to_index(index, page, txt)
			#scraps all the links for further crawling
			links = get_all_links(soup)
			graphs[page] = links
			union(to_crawl, links)
			crawled.append(page)
	return index, graphs


def get_all_links(page):
	links = []
	#get all links having a herf
	tags = page.find_all('a')

	for tag in tags:
		url = tag.get('href')
		if url:
			if url[0:4] == "http":
				links.append(url)
	return links

def union(links, page):
	#append the unique link to to_be_crawled list
	for link in page:
		if link not in links:
			links.append(link)

def add_page_to_index(index, url, content):
	#converting the text to a list of words
	content = clean(content)
	for word in content:
		add_to_index(index, word, url)

def add_to_index(index, keyword, url):
	#unique keyword or url gets appended to index
    if keyword in index:
    	if url not in index[keyword]:
        	index[keyword].append(url)
    else:
    	index[keyword] = []
    	index[keyword].append(url)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None#if no keyword found

def open_browser(url):
	webbrowser.open(url)#opens the url in the webbrowser

def look(index, key):
	for keyword in index:
		if key == keyword[0:1]:
			return index[keyword]

def compute_ranks(graph):
	d = 0.8
	numloops = 10

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0/npages

	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			newrank = (1-d)/npages
			for node in graph:
				if page in graph[node]:
					newrank = newrank + d*(ranks[node]/len(graph[node]))

			newranks[page] = newrank

		ranks = newranks
	return ranks


def geturl(urls, ranks):
	url = urls[0]
	for link in urls:
		if(ranks[link] > ranks[url]):
			url = link
	return url



def search():
	key = input()
	List = ['.com/' , '.org/' , '.net/']
	flag = False
	for extension in List:
		try:
			url = 'https://' + key + extension
			request = urllib.request.Request(url)
			opener = urllib.request.build_opener()
			response = opener.open(request)
			open_browser(url)
			flag = True
			break
		except URLError:
			continue
		except HTTPError:
			continue

	if flag == False:
		index, graphs = crawl_web('https://www.dictionary.com/')
		ranks = compute_ranks(graphs)
		#search for keyword in the dictionary
		urls = lookup(index, key)
		'''if(urls):
			for link in urls:
				print(1)
				print(link)s
				print(ranks[link])'''
		#if keyword is found
		if(urls):
			if(len(urls) > 1):
				url = geturl(urls, ranks)
			else:
				url = urls[0]
			#open the url containing the keyword in the browser
			open_browser(url)
		else:
			key = str(key[0:1])
			#search for similar results
			urls = look(index,key)
			if(len(urls) > 1):
				url = geturl(urls,ranks)
			else:
				url = urls[0]
			'''if(urls):
				for link in urls:
					print(link)
					print(ranks[link])'''
			#url = urls[-1]
			open_browser(url)

def main():
	search()

if __name__ == '__main__':
    main()
