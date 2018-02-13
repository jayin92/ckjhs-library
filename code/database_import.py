import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

### set up google drive api ###
scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
###############################

borrowSheet = client.open('圖書總表').worksheet('借閱總表')
bookSheet = client.open('圖書總表'). worksheet('書籍總表')
bookData = bookSheet.get_all_records()
borrowData = borrowSheet.get_all_records()
userSheet = client.open('圖書總表'). worksheet('借閱人總表')
userData = userSheet.get_all_records()

conn = sqlite3.connect('library.db')
c = conn.cursor()
borrowList = []
userList = []
bookList = []
for data in borrowData[0:]:
	username    = str(data['借閱人'])
	userid      = str(data['借閱人班級座號'])
	borrowtime  = str(data['借閱時間'])
	title       = str(data['借閱書籍'])
	isbn        = str(data['ISBN'])
	returntime  = str(data['歸還時間'])

	imformation = (username, userid, borrowtime, title, isbn, returntime)
	borrowList.append(imformation)

for data in userData[0:]:
	userid = str(data['班級座號'])
	username = str(data['姓名'])

	imformation = (userid, username)
	userList.append(imformation)

for data in bookData[0:]:
	title    = str(data['書籍名稱'])
	author   = str(data['作者'])
	pubtime  = str(data['出版年份'])
	isbn     = str(data['ISBN'])
	borrowid = str(data['借出'])

	imformation = (title, author, pubtime, isbn, borrowid)
	bookList.append(imformation)


c.execute('DELETE FROM borrow')
c.execute('DELETE FROM user')
c.execute('DELETE FROM book')

print('exporting...')
c.executemany('INSERT INTO borrow VALUES (?,?,?,?,?,?)', borrowList)
c.executemany('INSERT INTO user VALUES (?,?)', userList)
c.executemany('INSERT INTO book VALUES (?,?,?,?,?)', bookList)

conn.commit()

conn.close()
