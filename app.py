import os
import zipfile
from flask import Flask, render_template, request, redirect, send_file, flash, url_for, jsonify
import requests
from io import BytesIO
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = os.urandom(24)

YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources'

# Настройка кэша (можно использовать Redis для продакшн окружения)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})


# Главная страница для ввода публичной ссылки
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        public_key = request.form.get('public_key')
        return redirect(url_for('list_files', public_key=public_key))
    return render_template('index.html')


# Функция фильтрации файлов по типу
def filter_files(files, file_type=None):
    if file_type == 'images':
        return [f for f in files if f['mime_type'].startswith('image')]
    elif file_type == 'documents':
        return [f for f in files if f['mime_type'] in ['application/pdf', 'application/msword',
                                                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document']]
    return files


# Получение файлов с кэшированием
@app.route('/files', methods=['GET'])
@cache.cached(query_string=True)  # Кэширование по запросу
def list_files():
    public_key = request.args.get('public_key')
    file_type = request.args.get('file_type', 'all')  # Фильтр по типу файла

    response = requests.get(YANDEX_DISK_API_URL, params={'public_key': public_key})
    if response.status_code == 200:
        files = response.json().get('_embedded', {}).get('items', [])
        filtered_files = filter_files(files, file_type)
        return render_template('files.html', files=filtered_files, public_key=public_key)
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


# Скачивание нескольких файлов
@app.route('/download_multiple', methods=['POST'])
def download_multiple_files():
    file_urls = request.form.getlist('file_urls')
    file_names = request.form.getlist('file_names')

    if not file_urls or not file_names:
        flash('Вы не выбрали файлы для загрузки.')
        return redirect(url_for('list_files'))

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for url, name in zip(file_urls, file_names):
            response = requests.get(url)
            if response.status_code == 200:
                zf.writestr(name, response.content)

    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, download_name='files.zip', mimetype='application/zip')


if __name__ == '__main__':
    app.run(debug=True)

