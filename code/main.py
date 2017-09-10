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
# borrowSheet.resize(1)
borrowSheet = client.open('圖書總表').worksheet('借閱總表')
userSheet = client.open('圖書總表'). worksheet('借閱人總表')
bookSheet = client.open('圖書總表'). worksheet('書籍總表')
userData = userSheet.get_all_records()
bookData = bookSheet.get_all_records()
userName = ''
while True:
	userNum = int(input('請輸入學號 >'))
	if len(userName) == 0:
		for item in userData:
			if item['學號'] == userNum:
				userName = item['姓名']
				exit_flag = False
				break
	if exit_flag is True:
		print("沒有找到您的資料, 請在重新輸入一次")

	if exit_flag is False:
		exit_flag = True
		print('歡迎'+userName+'同學, 今天要借什麼書呢？')
		isbn = int(input("請刷條碼或輸入q取消借書 >"))
		if isbn == 10:
			print("再見"+userName+"同學")
			exit_flag = True
		userBook = ''
		for book in bookData:
			if book['ISBN'] == isbn:
				userBook = book
				exit_flag = False
		if exit_flag is True:
			print('找不到這本書, 請確認ISBN是否正確')
		if exit_flag is False:
			print(userBook)
			print('書籍名稱: '+userBook['書籍名稱'])
			check = input('確認借閱請輸入y, 取消輸入n')
			if check == 'y':
				borrowinfo = [userName, time.strftime(fmt), userBook['書籍名稱'], userBook['ISBN']]
				borrowSheet.append_row(borrowinfo)
			else:
				print('已取消')
