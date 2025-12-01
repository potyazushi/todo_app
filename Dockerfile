# Pythonイメージをベースにする
FROM python:3.11-slim

# コンテナ内の作業ディレクトリ
WORKDIR /app

# 依存関係をコピー＆インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースコードをコピー
COPY . .

# FastAPI起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
