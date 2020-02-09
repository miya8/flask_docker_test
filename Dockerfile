# ベースイメージとして docker公式イメージの python v3.7 を使用する
FROM python:3.7

# 以降のコマンドで使われる作業ディレクトリを指定する
WORKDIR /app

# カレントディレクトリにあるデータをコンテナ上の ｢/app｣ ディレクトリにコピーする
ADD . /app

# python製の自作アプリに必要なパッケージを インストール
RUN pip install -r requirements.txt

# Dockerに対してポート5000で待受けするよう指定
EXPOSE 5000

# コンテナが起動したときに実行される命令を指定する
CMD ["python", "test.py"]
