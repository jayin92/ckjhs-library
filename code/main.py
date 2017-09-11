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
userSheet = client.open('圖書總表'). worksheet('借閱人總表')
userData = userSheet.get_all_records()
def updateSheet():
	global borrowSheet, bookSheet, borrowData, bookData
	borrowSheet = client.open('圖書總表').worksheet('借閱總表')
	bookSheet = client.open('圖書總表'). worksheet('書籍總表')
	bookData = bookSheet.get_all_records()
	borrowData = borrowSheet.get_all_records()
userName = ''
borrowBook = False
os.system(clean)
print('請稍後...正在從Google Drive載入資料')
updateSheet()
mode = 'b'
conti = ''
contiReturn = ''
while True:
	os.system(clean)
	if conti == 'y':
		mode = 'b'
	elif contiReturn == 'y':
		mode = 'r'
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
			print('請稍後...正在從Google Drive載入資料')
		else:
			print('歡迎'+userName+'同學, 今天要借什麼書呢？')
			isbn = input("請刷條碼或輸入 q 取消借書 >")
		if isbn == 'q':
			os.system(clean)
			print("再見"+userName+"同學")
			updateSheet()
			os.system(clean)
			print('請稍後...正在從Google Drive載入資料')
			userName = ''
			isbn = ''
			userBook = 'pass'
		userBook = ''
		row = 2

		for book in bookData:
			if str(book['ISBN']) == isbn:
				userBook = book
				break
			row += 1
		if len(userBook) == 0 and len(userName) != 0:
			os.system(clean)
			print('找不到這本書, 請確認ISBN是否正確')
			time.sleep(2)
		elif not len(str(userBook['借出'])) == 0:
			os.system(clean)
			print(userBook['書籍名稱']+'已被'+str(userBook['借出'])+'借出')
			print('請選擇其他書籍 ：）')
			conti = ''
			userName = ''
			time.sleep(2)
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
				print('請稍後...正在上傳資料到Google Drive')
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
			time.sleep(2)
		else:
			i = 2
			for item in borrowData:
				if str(item['借閱人班級座號']) == userNum and len(borrowSheet.cell(i,6).value) == 0:
					rentBookList=[item['借閱書籍'], item['ISBN']]
					rentBook.append(rentBookList)
				i += 1
			if len(rentBook) == 0:
				os.system(clean)
				print('您沒有已借閱的書, 先去借書再來吧 ：）')
				contiReturn = ''
				time.sleep(2)
			else:
				os.system(clean)
				print(userName+'同學您好')
				print('您借的書如下：')
				for item in rentBook:
					print(item)
				returnBook = input('若要歸還,請刷書的條碼或輸入q取消 >')
				if returnBook == 'q':
					print('已取消')
				else:
					i = 2
					haveRentBook = False
					for book in rentBook:
						if book[1] == int(returnBook):
							haveRentBook = True
							print('您確定您要歸還 '+book[0]+' 嗎？')
							confirm = input('確定輸入y, 取消輸入 n > ')
							if confirm == 'y':
								i = 2
								for item in borrowData:
									if book[1] == item['ISBN']and len(borrowSheet.cell(i,6).value) == 0:
										borrowSheet.update_cell(i,6,time.strftime(fmt))
									i += 1
								i = 2
								for item in bookData:
									if book[1] == item['ISBN']:
										bookSheet.update_cell(i,5,'')
									i += 1
								updateSheet()
								print('請稍後...正在更新資料')
								os.system(clean)
								print('已成功歸還 '+book[0])
								contiReturn = input('還有要歸還的書嗎？, 有請輸入 y, 無則輸入 n >')
								if not contiReturn == 'y':
									userName = ''
								rentBook = []
							else:
								print('已取消')
								userName = ''
								time.sleep(2)
						elif i-1 == len(rentBook) and haveRentBook is False:
							print('沒有在您的借閱紀錄中找到這本書, 請重新掃條碼')
							contiReturn = 'y'
							time.sleep(2)
						i += 1
