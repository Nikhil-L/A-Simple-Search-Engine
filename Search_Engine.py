
import webbrowser
import requests
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from tkinter import*

def get_page(url):
	
	response = requests.get(url)
	page = response.text
	return page

def clean(content):
	content = word_tokenize(content)
	content = [word.lower() for word in content if word.isalpha()]
	stop_words = set(stopwords.words('english'))
	stop_words.add("this")
	stemmer = SnowballStemmer("english")
	i = 0
	for word in content:
		if(word not in stop_words):
			content[i] = stemmer.stem(word)
			i = i + 1
		else:
			del content[i]
	return content
	
def crawl_web(seed_page):

	to_crawl = [seed_page]
	crawled = []
	next_depth = []
	index = {}
	num = 0
	while to_crawl and num <= 3:
		page = to_crawl.pop()
		num = num + 1
		if(len(to_crawl) > 150):
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

def look(index, key):
	for keyword in index:
		if key == keyword[0:1]:
			return index[keyword]

def search():
	print("reached search")
	crawled, index = crawl_web('https://xkcd.com/')
	#for key in index:
		#print(key)
	stemmer = SnowballStemmer("english")
	key = entry.get()
	key = key.lower()
	key = stemmer.stem(key)
	urls = lookup(index, key)
	if(urls):
		urls = set(urls)
		url = urls.pop();
		open_browser(url)
	else:
		key = str(key[0:1])
		url = look(index,key)
		url = set(url)
		open_browser(url.pop())

entry = 0

def open_tkinter():
	my_window = Tk()
	label1 = Label(my_window, text = "Enter key word")
	global entry
	entry = Entry(my_window)
	button1 = Button(my_window, text = "click here to continue",command=search)

	label1.grid(row = 0, column = 0)
	entry.grid(row = 0, column = 1)
	button1.grid(row = 1)

	my_window.mainloop()

def main():
	open_tkinter()

if __name__ == '__main__':
    main()
    