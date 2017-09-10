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
	global borrowSheet, userSheet, bookSheet, userData, bookData
	borrowSheet = client.open('圖書總表').worksheet('借閱總表')
	userSheet = client.open('圖書總表'). worksheet('借閱人總表')
	bookSheet = client.open('圖書總表'). worksheet('書籍總表')
	userData = userSheet.get_all_records()
	bookData = bookSheet.get_all_records()
userName = ''
borrowBook = False
os.system(clean)
updateSheet()
while True:
	while True:
		if len(userName) == 0:
			userNum = input('請輸入學號 >')
			for item in userData:
				if str(item['學號']) == userNum:
					userName = item['姓名']
					exit_flag = False
					os.system(clean)
					break
		if len(userName) == 0:
			print("沒有找到您的資料, 請在重新輸入一次")
			break
		exit_flag = True
		print('歡迎'+userName+'同學, 今天要借什麼書呢？')
		isbn = input("請刷條碼或輸入 q 取消借書 >")
		if isbn == 'q':
			os.system(clean)
			print("再見"+userName+"同學")
			updateSheet()
			os.system(clean)
			userName = ''
			break

		userBook = ''
		for book in bookData:
			if str(book['ISBN']) == isbn:
				userBook = book
				exit_flag = False
		if exit_flag is True:
			os.system(clean)
			print('找不到這本書, 請確認ISBN是否正確')
		if exit_flag is False:
			os.system(clean)
			print('書籍名稱: '+userBook['書籍名稱'])
			print('作者: '+userBook['作者'])
			check = input('確認借閱請輸入 y , 取消輸入 n > ')
			if check == 'y':
				borrowinfo = [userName, time.strftime(fmt), userBook['書籍名稱'], userBook['ISBN']]
				os.system(clean)
				print('已成功借書')
				print('借閱人: '+userName)
				print('借閱書籍: '+userBook['書籍名稱'])
				print('借閱時間: '+time.strftime(fmt))
				borrowSheet.append_row(borrowinfo)
				updateSheet()
			else:
				os.system(clean)
				print('已取消')
