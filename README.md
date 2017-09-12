# 桃園市立建國國中數理資優班圖書管理系統
## 如何安裝及使用
**此程式是由Python語言寫成, 執行以下動作時請先確定是否安裝Python**,

下載Python(3.5.2版本, Windows 64位元)請[按我](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe)

安裝過程中務必將Python加入系統變數如下圖:

![Add Python 3.5 to PATH務必打勾](https://dbader-static-defugurjmqrkjo.netdna-ssl.com/figures/windows-setup-run-the-python-installer.jpg)

以上圖檔由
[此網站](https://dbader.org/blog/installing-python-and-pip-on-windows-10)提供

安裝後開啟命令提示字元(`Windows鍵 + R`後輸入`cmd`)開始輸入以下指令

若要執行此套件需要三個package, 分別是 `oauth2client`, `gspread`, `isbnlib` 安裝指令如下：

    pip install oauth2client gspread isbnlib

在執行程式之前請先參考
[此部影片](http://www.youtube.com/watch?v=https://youtu.be/vISRn5qFrkM?t=13s)

並依照影片指示建立屬於自己的 api 及`client_secret.json`

然後將`client_secret.json`放入`code`資料夾

最猴於自己的Google Drive建立名稱為 `圖書總表`的Google試算表並放入三個工作表, 分別為：

`借閱總表` , `借閱人總表`及 `書籍總表`

詳細格式請參考[建國國中數理資優班書籍管理系統網站](https://sites.google.com/view/ckjhsmath-book/%E5%9C%96%E6%9B%B8%E7%B8%BD%E8%A1%A8)

執行程式在code資料夾下執行以下指令：

    python main.py

或雙擊程式兩下

## 程式說明

所有程式我都已經放在code資料夾 分別有 `book.py` 及主程式`main.py`

`book.py` 用於加入新書

`main.py` 為借閱主程式
