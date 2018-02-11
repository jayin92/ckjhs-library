import gspread
from oauth2client.service_account import ServiceAccountCredentials
import isbnlib
import requests
import json
import time
import random
api_url = 'https://api.douban.com/v2/book/isbn/'

### GOOGLE API INITIALIZE ###
scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
sheet = client.open('圖書總表').worksheet('書籍總表')
#############################
######PROXY API INITIALIZE######
with open('proxy.txt', 'r+') as f:
	proxies = [line.strip() for line in f]

def get_proxy():
	return random.choice(proxies)

def delete_proxy(proxy):
	proxies.remove(proxy)
################################
global exit
global proxy
proxy = get_proxy()
def bookSearch(isbn):
	raw_data = requests.get(api_url+str(book), proxies={"https": "https://{}".format(proxy)})
	global book_data
	book_data = json.loads(raw_data.text)
	print(book_data)
	authors = book_data['author']
	pubdate = book_data['pubdate']
	isbncode = str(book_data['isbn13'])
	title = book_data['title']
	stringAuthor = ''
	for item in authors:
		stringAuthor = stringAuthor + item + ', '
	imformation = [title, stringAuthor, pubdate, isbncode]
	return imformation

while True:
	with open('books.txt', 'r') as f:
		books = [line.strip() for line in f]
	not_found = []
	success = []
	allBooks = len(books)
	currentBook = 1
	error_num = 1
	proxy = get_proxy()
	for book in books:
		try:
			data = bookSearch(book)
			print('success')
			success.append(data)
			books.remove(book)
		except:
			if 'code' in book_data and book_data['code'] == 6000:
				not_found.append(book)
				books.remove(book)
				print("not found")
			else:
				error_num += 1
				print("internet error")
		if error_num == 50:
			error = []
			delete_proxy(proxy)
			break

		print(str(currentBook)+'/'+str(allBooks))
		print("")
		currentBook += 1

	print("uploading...")
	success_num = len(success)
	i=0
	for item in success:
		i += 1
		print(str(i)+'/'+str(success_num))
		sheet.append_row(item)

	with open('books.txt', 'r+') as thefile:
		thefile.truncate()
		for item in books:
			thefile.write("%s\n" % item)

	with open("notfound.txt", 'w') as nt:
		for item in not_found:
			nt.write('%s\n' % item)

	print('已全部上傳')

	with open('proxy.txt','w') as f:
		for item in proxies:
			f.write('%s\n' % item)
