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

isbncode = input('請輸入isbn >')

data = bookSearch(isbncode)
print(sheet.get_all_records())
print(data)
sheet.append_row(data)
