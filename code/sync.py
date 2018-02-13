import sqlite3
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

### set up google drive api ###
scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
###############################
borrow_title = ['借閱人','借閱人班級座號','借閱時間','借閱書籍','ISBN','歸還時間']
user_title   = ['班級座號','姓名']
book_title   = ['書籍名稱','作者','出版年份','ISBN','借出']

start_time = time.time()
conn = sqlite3.connect('library.db')

borrowSheet = client.open('圖書總表').worksheet('借閱總表')
userSheet = client.open('圖書總表'). worksheet('借閱人總表')
bookSheet = client.open('圖書總表'). worksheet('書籍總表')

# borrowSheet.clear()
# userSheet.clear()
# bookSheet.clear()

def get_data_from_database(table):
	global conn
	c = conn.cursor()
	c.execute("SELECT * FROM "+table)
	rows = c.fetchall()
	return [list(t) for t in rows]

def update_data_to_cloud(list, sheet):
	for data in list:
		sheet.append_row(data)

borrowList = get_data_from_database('borrow')
userList   = get_data_from_database('user')
bookList   = get_data_from_database('book')
borrowList.insert(0,borrow_title)
userList.insert(0, user_title)
bookList.insert(0, book_title)

# update_data_to_cloud(borrowList, borrowSheet)
# update_data_to_cloud(userList, userSheet)
# update_data_to_cloud(bookList, bookSheet)
conn.close()
print(time.time()-start_time)
