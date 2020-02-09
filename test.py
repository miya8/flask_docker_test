# Flask などの必要なライブラリをインポートする
import os
from datetime import datetime

import werkzeug
from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request, url_for, send_from_directory)

import pandas as pd
import numpy as np
import settings.messages as msg
from settings.base import *

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
# limit upload file size : 1MB
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route("/")
def index():

    # 実際はファイルから取得するリスト
    shohin_list = [
        "product_1",
        "product_2",
        "product_3",
        "product_4",
        "product_5",
        "product_6",
        "product_7",
        "product_8",
        "product_9",
        "product_10",
    ]

    rank_dict = {
        key_str: zip([rank.lower() for rank in RANK_DICT[key_str]], RANK_DICT[key_str])
        for key_str in RANK_DICT.keys()
    }
    # jinja2の参考にさせていただいた: https://tanuhack.com/jinja2-cheetsheet/
    # index.html をレンダリングする
    return render_template("test.html",
                           title=SYSTEM_NAME,
                           message=msg.HOWTOUSE,
                           rank_dict=rank_dict,
                           product_list=shohin_list
                           )

# /post にアクセスしたときの処理
@app.route("/result", methods=["GET", "POST"])
def return_result():
    if request.method == "POST":
        # リクエストフォームから「名前」を取得
        name = request.form.get("name")
        # チェックボックスで選択された項目のリストを取得
        checked_list = request.form.getlist("chk_rank")
        # 選択された商品のリストを取得
        selected_shohin_list = request.form.get("txt_shohin_selected")

        # アップロードされたファイルを取得
        if not "upload_files" in request.files:
            return make_response(jsonify({"result':'upload_files not exist."}))
            
        files = request.files.getlist("upload_files")
        for f in files:
            saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
                + werkzeug.utils.secure_filename(f.filename)
            #saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_")
            f.save(os.path.join(UPLOAD_DIR, saveFileName))
        print(f"name: {name}")
        print(f"checked_list: {checked_list}")
        print(f"selected_shohin_list: {selected_shohin_list}")
        # index.html をレンダリングする
        # 実際は別処理で取得するテーブル
        df = pd.DataFrame(
            {
                "product": np.random.choice(selected_shohin_list.split(","), size=20),
                "rank": np.random.choice(RANK_DICT.get("a") + RANK_DICT.get("b"), size=20)
            }
        )
        save_file_name = "{}.csv".format(datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        download_file_name = "result_" + save_file_name
        df.to_csv(os.path.join(DOWNLOAD_DIR, save_file_name), index=False)
        #return render_template("test.html", name=name)
        #今回はcsvだが、ExcelのMIMETYPE参考ページ：https://qiita.com/5zm/items/760000cf63b176be544c
        return send_from_directory(
            DOWNLOAD_DIR,
            save_file_name,
            as_attachment = True,
            attachment_filename = download_file_name,
            mimetype = "text/csv"
            )
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for("result"))


if __name__ == "__main__":
    app.debug = True  # デバッグモード有効
    # hostはデフォルトでループバックアドレスだが、未来の自分が気にしそうなので明示しておく
    # 本番環境では run を使用しないように注意喚起されている（セキュリティ関連）
    # 公式ドキュメント: https://flask.palletsprojects.com/en/1.0.x/api/
    #app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
