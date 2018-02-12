# coding=<UTF-8>

### import library ###
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import platform
import os

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

def updateSheet():
	global borrowSheet, bookSheet, borrowData, bookData, userSheet, userData
	borrowSheet = client.open('圖書總表').worksheet('借閱總表')
	bookSheet = client.open('圖書總表'). worksheet('書籍總表')
	bookData = bookSheet.get_all_records()
	borrowData = borrowSheet.get_all_records()
	userSheet = client.open('圖書總表'). worksheet('借閱人總表')
	userData = userSheet.get_all_records()

def yes_or_no(question):
	reply = str(input(question+' (y/n): ')).lower().strip()
	if reply[0] == 'y':
		return True
	if reply[0] == 'n':
		return False
	else:
		return yes_or_no("請輸入 y 或 n")
#############################################
def get_user_name():
	global userName, userID
	userName = ''
	userID = input("輸入學號 >")
	for student in userData:
		if str(student['班級座號']) == userID:
			userName = student['姓名']
	if userName == '':
		os.system(clean)
		print('沒有找到您的資料, 請再重新輸入一次')
		updateSheet()
		print('請稍後...正在從Google Drive載入資料')
		check_user_name()
def borrow_book():
	global isbn
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
			if str(book['ISBN']) == isbn:
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
		elif not str(userBook['借出']) == '':
			os.system(clean)
			print(userBook['書籍名稱']+'已被'+str(userBook['借出'])+'借出')
			print('請選擇其他書籍 ：）')
			borrow_book()
		else:
			confirm_borrow()

def add_new_book():
	global userBook
	title = str(input('書名: '))
	author = str(input('作者: '))
	isbn_confirm = input('請再掃描一次條碼: ')
	if not str(isbn_confirm) == str(isbn):
		print("條碼不一致, 請重新輸入一次")
		time.sleep(3)
		add_new_book()
	else:
		new_book=[title, author, '', isbn]
		userBook = {'書籍名稱':title,'作者':author,'ISBN':isbn}

		row = bookSheet.row_count + 1
		add_book = True
		confirm_borrow()
def confirm_borrow():
	global add_book
	os.system(clean)
	print(type(userBook))
	print(userBook)
	if add_book is True:
		add_book = False
		bookSheet.append_row(new_book)
	print('書籍名稱: '+userBook['書籍名稱'])
	print('作者: '+userBook['作者'])
	if yes_or_no("確定要借閱嗎?"):
		borrowinfo = [userName, userID, time.strftime(fmt), userBook['書籍名稱'], userBook['ISBN']]
		os.system(clean)
		borrowSheet.append_row(borrowinfo)
		bookSheet.update_cell(row, 5, userID)
		print('已成功借書')
		print('借閱人: '+userName)
		print('借閱書籍: '+userBook['書籍名稱'])
		print('借閱時間: '+time.strftime(fmt))
		if yes_or_no("還要繼續借書嗎"):
			borrow_book()
		else:
			print('感謝使用此系統')
			sleep(3)
			main()
	else:
		if yes_or_no('有要借其他書嗎?'):
			borrow_book()
		else:
			print('感謝使用此系統')
			time.sleep(2)
			main()

def main():
	global add_book
	add_book = False
	os.system(clean)
	print('請稍後...正在從Google Drive載入資料')
	updateSheet()
	os.system(clean)
	mode = input('b : 借書, r : 還書 >')
	if mode == 'b':
		get_user_name()
		print('歡迎'+userName+'同學, 今天要借什麼書呢？')
		borrow_book()

	elif mode == 'r':
		print('r')
	else:
		os.system(clean)
		print("請輸入 b 或 r")
		main()

main()
