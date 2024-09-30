# Веб-приложение для работы с Яндекс.Диском

Это Flask-приложение позволяет просматривать и скачивать файлы с Яндекс.Диска по публичной ссылке.

## Установка и запуск

# 1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/IsaacTroevsky/MycegoTest.git
   cd MycegoTest
   ```
# 2. Создайте и активируйте виртуальное окружение:

Windows: 
 ```bash python -m venv venv
.\venv\Scripts\activate
```

macOS/Linux:
 ```bash python3 -m venv venv
source venv/bin/activate
```
# 3. Установите зависимости:
 ```bash
 pip install -r requirements.txt
 ```
# 4. Запустите приложение
```bash
python app.py
```
# 5. Откройте браузер и перейдите по адресу:
```bash
http://127.0.0.1:5000/
```

Возможности
 - Просмотр файлов по публичной ссылке.
 - Фильтрация файлов по типам.
 - Скачивание выбранных файлов.
