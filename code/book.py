import gspread
from oauth2client.service_account import ServiceAccountCredentials
import isbnlib


def bookSearch(isbn):
	result = isbnlib.meta(isbn, service='goob')
	title = result['Title']
	authors = result['Authors']
	year = result['Year']
	isbncode = str(result['ISBN-13'])
	stringAuthor = ''
	for item in authors:
		print(item)
		stringAuthor = stringAuthor + item + ', '

	imformation = [title, stringAuthor, year, isbncode]
	return imformation

scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)

sheet = client.open('圖書總表').worksheet('書籍總表')

# isbncode = input('請輸入isbn >')
with open('books.txt', 'r') as f:
    books = [line.strip() for line in f]

error = []
for book in books:
	try:
		data = bookSearch(book)
		print(data)
		sheet.append_row(data)
	except:
		error.append(book)
print('已全部上傳')
print(error)
