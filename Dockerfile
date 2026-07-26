#Dockerfile
#Project to build epub converter in Docker using Python, Flask, Open

# 使用官方的 Python 基本映像作為基礎映像
FROM python:3.12-slim

# 設置工作目錄（如果目錄不存在，WORKDIR 會自動建立）
WORKDIR /app

# 複製當前目錄下的所有內容到映像的 /app 目錄下
COPY . /app
#更新pip工具軟體至最新
RUN pip install --upgrade pip
#依需求檔requirements.txt安裝所需軟體
# 安裝 Flask,opencc …
RUN pip install --no-cache-dir -r requirements.txt
#更新apt工具軟體至最新，注意使用空間較大。
#RUN apt update -y
#使用apt安裝軟體
#RUN apt install curl -y

# Expose the port your app runs on (e.g., 5000 for Flask)
#EXPOSE 5555

# 執行應用
CMD  ["python", "app.py"]
#CMD  ["uvicorn", "app2:app", "--host", "0.0.0.0", "--port", "5555"]

#其它備註說明
#禁用快取: --no-cache-dir 標誌指示 pip 不要使用其內部快取。
#影響:
#構建時間可能更長: 因為 pip 需要在每次構建時再次下載每個套件，這可能會顯著增加構建時間。
#確保一致的構建: 通過禁用快取，您可以確保每次構建都使用完全相同的套件版本，即使 PyPI 伺服器上有套件更新。這對於可重複性和調試至關重要。

#method-1:
#Build Docker image
# Docker image build -t OrzXD1/py_flask_opencc:v1.0.0 .

#Run Docker image in Containers
#—Using volume v2 to store /app/. data
#—outside port is 8088
# docker run -d -p 8088:5555 --name tank-web-new --volume v2:/app OrzXD1/py_flask_opencc:v1.0.1

#method-2:
#docker image build -t app-local -f Dockerfile.local .
#使用host主機執行目錄pwd映射/app目錄,方便debug
#docker run -d -it -p 8088:5000 --name flask-web-new -v $(pwd):/app app-local




