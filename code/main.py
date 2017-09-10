# coding=<UTF-8>

import gspread
import time
import isbnlib
from oauth2client.service_account import ServiceAccountCredentials
import platform
import os


if platform.system() == 'Windows':
	clean = 'cls'
else:
	clean = 'clear'

scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
mode = 2
exit_flag = True
fmt = '%Y/%m/%d %H:%M:%S'
isbn = ''
# borrowSheet.resize(1)
def updateSheet():
	global borrowSheet, userSheet, bookSheet, userData, bookData, borrowData
	borrowSheet = client.open('圖書總表').worksheet('借閱總表')
	userSheet = client.open('圖書總表'). worksheet('借閱人總表')
	bookSheet = client.open('圖書總表'). worksheet('書籍總表')
	userData = userSheet.get_all_records()
	bookData = bookSheet.get_all_records()
	borrowData = borrowSheet.get_all_records()
userName = ''
borrowBook = False
os.system(clean)
updateSheet()
mode = 'b'
conti = ''
while True:
	os.system(clean)
	if conti == 'y':
		mode = 'b'
	else:
		mode = input('輸入b來借書, r來還書 >')
	if mode == 'b':
		if len(userName) == 0:
			userNum = input('請輸入班級座號(五碼) >')
			for item in userData:
				if str(item['班級座號']) == userNum:
					userName = item['姓名']
					exit_flag = False
					os.system(clean)
		if len(userName) == 0:
			print("沒有找到您的資料, 請再重新輸入一次")
			updateSheet()
		else:
			print('歡迎'+userName+'同學, 今天要借什麼書呢？')
			isbn = input("請刷條碼或輸入 q 取消借書 >")
		if isbn == 'q':
			os.system(clean)
			print("再見"+userName+"同學")
			updateSheet()
			userName = ''
			isbn = ''
			# mode = ''
		userBook = ''
		row = 1
		for book in bookData:
			if str(book['ISBN']) == isbn:
				userBook = book
				break
			row += 1
		if len(userBook) == 0:
			os.system(clean)
			print('找不到這本書, 請確認ISBN是否正確')
		elif not len(userBook['借出']) == 0:
			os.system(clean)
			print(userBook['書籍名稱']+'已被'+str(userBook['借出'])+'借出')
			print('請選擇其他書籍 ：）')
			time.sleep(5)
		else:
			os.system(clean)
			print('書籍名稱: '+userBook['書籍名稱'])
			print('作者: '+userBook['作者'])
			check = input('確認借閱請輸入 y , 取消借閱輸入 n > ')
			if check == 'y':
				borrowinfo = [userName, userNum, time.strftime(fmt), userBook['書籍名稱'], userBook['ISBN']]
				os.system(clean)
				borrowSheet.append_row(borrowinfo)
				bookSheet.update_cell(row, 5, userNum)
				updateSheet()
				print('已成功借書')
				print('借閱人: '+userName)
				print('借閱書籍: '+userBook['書籍名稱'])
				print('借閱時間: '+time.strftime(fmt))
				conti = input('還有要借書嗎？, 有 請輸入y, 沒有 輸入n >')
				isbn = ''
				userBook = ''
				if not conti == 'y':
					userName = ''
			else:
				os.system(clean)
				print('已取消')
	if mode == 'r':
		rentBook = []
		if len(userName) == 0:
			userNum = input('請輸入班級座號(五碼) >')
		for item in userData:
			if str(item['班級座號']) == userNum:
				userName = item['姓名']
				exit_flag = False
				os.system(clean)
				break
		if len(userName) == 0:
			print("沒有找到您的資料, 請再重新輸入一次")
		else:
			for item in borrowData:
				if str(item['借閱人班級座號']) == userNum:
					rentBook.append(item['借閱書籍'])
			if len(rentBook) == 0:
				os.system(clean)
				print('您沒有已借閱的書, 先去借書再來吧 ：）')
			else:
				print('您借的書如下：')
				for item in rentBook:
					print(item)
				time.sleep(5)
