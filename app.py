import os
from flask import Flask, render_template, request, redirect, send_file, flash, url_for
import requests
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Для хранения сессий

YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

# Главная страница для ввода публичной ссылки
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        public_key = request.form.get('public_key')
        return redirect(url_for('list_files', public_key=public_key))
    return render_template('index.html')

# Страница со списком файлов
@app.route('/files', methods=['GET'])
def list_files():
    public_key = request.args.get('public_key')
    response = requests.get(YANDEX_DISK_API_URL, params={'public_key': public_key})
    if response.status_code == 200:
        files = response.json().get('_embedded', {}).get('items', [])
        return render_template('files.html', files=files, public_key=public_key)
    else:
        flash('Не удалось получить данные с Яндекс.Диска. Проверьте ссылку.')
        return redirect(url_for('index'))

# Скачивание файла
@app.route('/download', methods=['GET'])
def download_file():
    file_url = request.args.get('file_url')
    file_name = request.args.get('file_name')
    response = requests.get(file_url)
    if response.status_code == 200:
        return send_file(BytesIO(response.content), as_attachment=True, download_name=file_name)
    else:
        flash('Не удалось загрузить файл.')
        return redirect(url_for('list_files'))

if __name__ == '__main__':
    app.run(debug=True)
