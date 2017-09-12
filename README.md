# 桃園市立建國國中數理資優班圖書管理系統
## 如何安裝及使用
**此程式是由Python語言寫成, 執行以下動作時請先確定是否安裝Python**,

下載Python(3.5.2版本, Windows 64位元)請[按我](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe)

安裝過程中務必將Python加入系統變數如下圖:
![Add Python 3.5 to PATH務必打勾](https://imgur.com/zDTWF)

安裝後開啟命令提示字元(`Windows鍵 + R`後輸入`cmd`)開始輸入以下指令

若要執行此套件需要三個package, 分別是 `oauth2client`, `gspread`, `isbnlib` 安裝指令如下：

    pip install oauth2client gspread isbnlib

在執行程式之前請先參考此部影片
[![Youtube Video](http://img.youtube.com/vi/https://youtu.be/vISRn5qFrkM?t=13s/0.jpg)](http://www.youtube.com/watch?v=https://youtu.be/vISRn5qFrkM?t=13s)
## 程式說明

所有程式我都已經放在code資料夾 分別有 `book.py` 及主程式`main.py`

`book.py` 用於加入新書

`main.py` 為借閱主程式
