# coding=<UTF-8>

### import library ###
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import platform
import os
from terminaltables import SingleTable, AsciiTable
from termcolor import colored, cprint
import sqlite3
### confirm operating system ###
if platform.system() == 'Windows':
	clean = 'cls'
else:
	clean = 'clear'

### set up google drive api ###
scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
###############################

### set up variables ###
fmt = '%Y/%m/%d %H:%M:%S'
isbn = ''


### get data sheet from google drive ###
conn = sqlite3.connect('library.db')
c = conn.cursor()

def update_google_drive():
	global borrowSheet, userSheet, bookSheet
	borrowSheet = client.open('圖書總表').worksheet('借閱總表')
	userSheet = client.open('圖書總表'). worksheet('借閱人總表')
	bookSheet = client.open('圖書總表'). worksheet('書籍總表')
def get_data_from_database(table):
	global conn
	c = conn.cursor()
	c.execute("SELECT * FROM "+table)
	rows = c.fetchall()
	return [list(t) for t in rows]
def update_database():
	global borrowData, bookData, userData         #    0        1         2          3      4          5
	borrowData = get_data_from_database('borrow') # username, userid, borrow_time, title, isbn,   return_time
	userData  = get_data_from_database('user')    # username, userid
	bookData  = get_data_from_database('book')    # title,    author, pubtime,     isbn,  borrowid

def yes_or_no(question):
	reply = str(input(question+' (y/n): ')).lower().strip()
	if reply[0] == 'y':
		return True
	if reply[0] == 'n':
		return False
	else:
		return yes_or_no("請輸入 y 或 n")
def print_table(list, title=None):
	print(AsciiTable(list, title).table)
def color_list(list, color):
	return [colored(item, color) for item in list]
#############################################
def get_user_name():
	global userName, userID, conn, c
	userName = ''
	userID = input("請輸入班級座號(五碼) >")
	c.execute("SELECT username FROM user WHERE userid=?", (userID,))
	userName = c.fetchone()[0]

	if userName == '':
		os.system(clean)
		print('沒有找到您的資料, 請再重新輸入一次')
		update_database()
		print('正在載入資料...')
		get_user_name()
def get_borrow_book(id):
	returnList = []
	for data in borrowData:
		if id == str(data[1]) and data[5] == '':
			title = data[3]
			time = data[2]
			isbn = data[4]
			returnList.append([title, time, isbn])
	returnList.insert(0,['借閱書籍', '借閱時間', 'ISBN'])
	return returnList
def borrow_book():
	global isbn, userName
	isbn = input('請刷條碼或輸入 q 取消借書 >')
	if isbn == 'q':
		os.system(clean)
		print("再見"+userName+"同學")
		time.sleep(2)
		main()
	else:
		global userBook, row
		userBook = ''
		row = 2
		add_book = False
		for book in bookData:
			if str(book[3]) == isbn:
				userBook = book
				break
			row += 1
		if userBook == '':
			print('資料庫中找不到這本書, 請確認ISBN是否正確')
			if yes_or_no("要自行輸入書的資料嗎並借出嗎") is True:
				add_new_book()
			elif yes_or_no("要借其他本書嗎"):
				borrow_book()
			else:
				main()
		elif not str(userBook[4]) == '':
			os.system(clean)
			print(userBook[0]+'已被'+str(userBook[4])+'借出')
			print('請選擇其他書籍 ：）')
			borrow_book()
		else:
			confirm_borrow()
def multi_borrow_book():
	global borrowList
	os.system(clean)
	print_table(borrowList)
	isbn = str(input('請掃描欲借閱書籍條碼, 掃描完成輸入 y, 取消借閱輸入 n '+'(已輸入'+str(len(borrowList)-1)+ ')>'))
	if isbn == 'y':
		confirm_borrow()
	elif isbn == 'n':
		main()
	else:
		for book in bookData:
			if isbn == str(book[3]):
				title = str(book[0])
				author = str(book[1])
				pubtime = str(book[2])
				if not str(book[4]) == '':
					print(title+'已被'+str(book[4])+'借出')
					print('請選擇其他書籍')
					time.sleep(1.5)
					multi_borrow_book()
				else:
					imformation = [title, author, pubtime, isbn]
					borrowList.append(imformation)
					multi_borrow_book()

		print('資料庫中找不到這本書, 請確認ISBN是否正確')
		if yes_or_no("要自行輸入書的資料嗎並借出嗎") is True:
			add_new_book()
		elif yes_or_no("要借其他本書嗎"):
			multi_borrow_book()
		else:
			print('感謝使用此系統')
			time.sleep(1)
			main()
def add_new_book():
	global userBook, bookSheet, conn
	c = conn.cursor()
	title = str(input('書名: '))
	author = str(input('作者: '))
	pubtime = str(input('出版日期(不知可不填): '))
	isbn_confirm = input('請再掃描一次條碼: ')
	if not str(isbn_confirm) == str(isbn):
		print("條碼不一致, 請重新輸入一次")
		time.sleep(3)
		add_new_book()
	else:
		new_book=(title, author, pubtime, isbn)
		c.execute("INSERT INTO borrow VALUES (?,?,?,?)", new_book)
		conn.commit()
		update_database()
		multi_borrow_book()
def confirm_borrow():
	global borrowList
	os.system(clean)
	print('欲借閱書籍:')
	print_table(borrowList)
	if yes_or_no("確定要借閱嗎?"):
		c = conn.cursor()
		borrowinfo = []
		for book in borrowList[1:]:
			borrowinfo.append((userName, userID, time.strftime(fmt), book[0], book[3], '')) #book[title, author, pubtime, isbn]
			c.execute("UPDATE book SET borrowid={} WHERE isbn={}".format(userID, book[3]))
		c.executemany('INSERT INTO borrow VALUES (?,?,?,?,?,?)', borrowinfo)
		conn.commit()
		update_database()
		os.system(clean)
		print('已成功借書')
		print_table(get_borrow_book(userID))
		if yes_or_no("還要繼續借書嗎"):
			borrow_book()
		else:
			print('感謝使用此系統')
			time.sleep(3)
			main()
	else:
		if yes_or_no('有要借其他書嗎?'):
			borrow_book()
		else:
			print('感謝使用此系統')
			time.sleep(2)
			main()
############################################
def get_rent_book():
	global userID, rentBook
	rentBook = []
	for item in borrowData:
		if str(item[1]) == userID and item[5] == '':
			rentBookList=[item[3], item[2], item[4]] #[title, borrow_time, isbn]
			rentBook.append(rentBookList)
	rentBook.insert(0,['已借閱書籍','借閱時間', 'ISBN'])

	return rentBook
def multi_return_book():
	global userName, rentBook, returnList
	os.system(clean)
	print('您借的書如下：')
	print_table(rentBook)
	returnISBN = str(input('請掃描欲歸還書籍條碼, 掃描完成輸入 y, 取消歸還輸入 n '+'(已輸入'+str(len(returnList)-1)+ ')>'))
	if returnISBN == 'y':
		confirm_return()
	elif returnISBN == 'n':
		main()
	else:
		for book in rentBook:
			if str(book[2]) == returnISBN:
				returnList.append(book)
		rentBook = [color_list(item,'green') if str(item[2]) == returnISBN else item for item in rentBook]

		multi_return_book()
def confirm_return():
	global borrowData, borrowSheet, bookData, bookSheet, rentBook, returnList, conn
	os.system(clean)
	print_table(returnList)
	if yes_or_no('確認要歸還以上的書嗎'):
		print('正在處理歸還資料...')
		c = conn.cursor()
		for book in returnList[1:]:
			print(book[1])
			sql = 'UPDATE borrow SET return_time="{}" WHERE "{}"=borrow_time AND {}=isbn'.format(time.strftime(fmt),book[1], book[2])
			print(sql)
			c.execute(sql)
			c.execute("UPDATE book SET borrowid='' WHERE {}=isbn".format(book[2]))
		conn.commit()
		update_database()
		os.system(clean)
		print('已成功歸還'+str(len(returnList)-1)+'本書')
		print('以下是您目前借閱的書')
		print_table(get_borrow_book(userID))
		print('感謝使用此系統')
		time.sleep(3)
		main()
	else:
		main()
def return_book():
			global rentBook, returnList
			get_rent_book()
			if len(rentBook)<2:
				os.system(clean)
				print('您沒有借閱的書, 先去借書再來吧 ：）')
				time.sleep(2)
				main()
			else:
				returnList = [['欲歸還書籍', '借閱時間', 'ISBN']]
				multi_return_book()

def main():
	global add_book, borrowList
	add_book = False
	os.system(clean)
	print('請稍後...正在從Google Drive載入資料')
	update_database()
	os.system(clean)
	get_user_name()
	print(userName+'同學您好')
	mode = input('b : 借書, r : 還書 >')
	if mode == 'b':
		borrowList = [['書籍名稱','作者','出版日期','ISBN']]
		multi_borrow_book()

	elif mode == 'r':
		return_book()

	else:
		os.system(clean)
		print("請輸入 b 或 r")
		main()


main()
