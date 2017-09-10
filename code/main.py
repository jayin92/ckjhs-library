# coding=<UTF-8>

import gspread
import time
import isbnlib
from oauth2client.service_account import ServiceAccountCredentials



scope = ['https://spreadsheets.google.com/feeds']
cred = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(cred)
mode = 2
exit_flag = True
fmt = '%Y/%m/%d %H:%M:%S'
isbn = ''
# borrowSheet.resize(1)
borrowSheet = client.open('圖書總表').worksheet('借閱總表')
userSheet = client.open('圖書總表'). worksheet('借閱人總表')
bookSheet = client.open('圖書總表'). worksheet('書籍總表')
userData = userSheet.get_all_records()
bookData = bookSheet.get_all_records()
userName = ''
borrowBook = False
while True:
	while True:
		if len(userName) == 0:
			userNum = int(input('請輸入學號 >'))
			for item in userData:
				if item['學號'] == userNum:
					userName = item['姓名']
					exit_flag = False
					break
		if len(userName) == 0:
			print("沒有找到您的資料, 請在重新輸入一次")
			break
		exit_flag = True
		if borrowBook is False:
			print('歡迎'+userName+'同學, 今天要借什麼書呢？')
		isbn = int(input("請刷條碼或輸入q取消借書 >"))
		if isbn == 10:
			print("再見"+userName+"同學")
			userName = ''
			borrowBook = False
			break

		userBook = ''
		for book in bookData:
			if book['ISBN'] == isbn:
				userBook = book
				exit_flag = False
		if exit_flag is True:
			print('找不到這本書, 請確認ISBN是否正確')
			borrowBook = True
		if exit_flag is False:
			print('書籍名稱: '+userBook['書籍名稱'])
			print('作者: '+userBook['作者'])
			check = input('確認借閱請輸入y, 取消輸入n')
			if check == 'y':
				borrowinfo = [userName, time.strftime(fmt), userBook['書籍名稱'], userBook['ISBN']]
				borrowSheet.append_row(borrowinfo)
			else:
				print('已取消')
