# app.py
from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
)
# from werkzeug.utils import secure_filename
# Import the blueprint object from your routes file
# from xepub import epub_s2twp  # Import your blueprint
# from users import user_admin

import os
import zipfile
import shutil
import opencc

# import http.server
# import socketserver
import cgi
import urllib.request

app = Flask(__name__)


# ---------------------------------------------------------------------------------------
# sub routine == convert_epub to convert .epub file from 簡體中文 to 台灣繁體中文
# 初始化 OpenCC 台灣繁體慣用語轉換器
cc = opencc.OpenCC("s2twp")


# 核心轉換邏輯
def convert_epub(input_path, output_path):
    temp_dir = "temp_web_epub"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    with zipfile.ZipFile(input_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith((".html", ".xhtml", ".ncx", ".opf", ".txt")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                converted_content = cc.convert(content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(converted_content)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zip_ref.write(full_path, rel_path)

    shutil.rmtree(temp_dir)


# ---------------------------------------------------------------------------------------


# show web page in this program
@app.route("/")
@app.route("/hi")
def hello():
    return "Say Hello World in app.py"


@app.route("/text")
def text():
    return "<html><body><h1>Say Hello World by html format in app.py</h1></body></html>"


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            uploaded_file.save(uploaded_file.filename)
        return redirect(url_for("upload"))
    return render_template("upload.html")


# show web page by redirect web page to /template
@app.route("/epub", methods=["GET", "POST"])
def xepub():
    if request.method == "POST":
        file_item = request.files["epub_file"]

        if file_item.filename:
            # 暫存上傳的檔案
            input_name = "uploaded_input.epub"
            output_name = "converted_output.epub"

            file_item.save(input_name)
            # with open(input_name, 'wb') as f:
            # f.write(file_item.file.read())

            # 執行 OpenCC 轉換
            convert_epub(input_name, output_name)
            print({input_name}, {output_name})
            # 將轉換後的檔案回傳給瀏覽器下載
            # self.send_response(200)
            # self.send_header("Content-type", "text/plain")
            # self.send_header("Content-Type", "application/epub+zip")
            # print(f"file_item.filename : {file_item.filename}")
            # 讓下載的檔名自動加上 [繁體]
            download_name = cc.convert(
                file_item.filename.replace("_zh.", ".")
                .replace('"', "")
                .replace("-1.epub", ".epub")
                .replace(" (z-library.sk, 1lib.sk, z-lib.sk)", "")
                .replace(".epub", "_zh.epub")
            )
            encoded_name = urllib.parse.quote(download_name)
            print(f"output-name : {download_name}")
            # print(f#encode-name : {encoded_name}")
            # header_value = f"attachment; filename=\"{download_name}\"; filename*=UTF-8''{encoded_name}"
            # header_value = f"attachment; filename*=UTF-8''{encoded_name}"
            # self.send_header("Content-Disposition", header_value)
            # self.end_headers()

            # with open(output_name, 'rb') as f:
            #    self.wfile.write(f.read())

            return send_file(
                output_name, as_attachment=True, download_name=download_name
            )

            # 清理本機暫存檔
            if os.path.exists(input_name):
                os.remove(input_name)
            if os.path.exists(output_name):
                os.remove(output_name)

        return redirect(url_for("xpub"), filename=output_name)

    return render_template("xepub.html")


@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name", "world"))
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/page/text")
def pageText():
    return render_template("page.html", text="Python Flask !")


@app.route("/page/app")
def pageAppInfo():
    appInfo = {  # dict
        "id": 5,
        "name": "Python - Flask",
        "version": "1.0.1",
        "author": "Enoxs",
        "remark": "Python - Web Framework",
    }
    return render_template("page.html", appInfo=appInfo)


@app.route("/page/data")
def pageData():
    data = {  # dict
        "01": "Text Text Text",
        "02": "Text Text Text",
        "03": "Text Text Text",
        "04": "Text Text Text",
        "05": "Text Text Text",
    }
    return render_template("page.html", data=data)


# below is show web page by using static html
@app.route("/static")
def staticPage():
    return render_template("static.html")


# Register the blueprint with the application
# epub_module = epub_bp()
# app.register_blueprint(epub_s2twp.blueprint,url_prefix='/api')
# app.register_blueprint(user_admin)


# define port is 5555
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)

# 在 main 方法的 app.run() 函式中，加上 0.0.0.0 的字串。
# 配置到產品的伺服器中，客戶端的電腦才能夠連接上網站的伺服器。

# Debug 模式
# 先前的程式碼中，任何的修改都必須要重新啟動。(網頁的程式碼也是如此)
