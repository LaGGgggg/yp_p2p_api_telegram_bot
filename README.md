# Telegram-бот API для p2p оценки проектов студентов в Яндекс практикуме

# Как запустить проект?

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/LaGGgggg/yp_p2p_api_telegram_bot.git
cd yp_p2p_api_telegram_bot
```

### 2. Создайте виртуальное окружение

#### С помощью [pipenv](https://pipenv.pypa.io/en/latest/):

```bash
pip install --user pipenv
pipenv shell  # create and activate
```

#### Или классическим методом:

```bash
python -m venv .venv  # create
.venv\Scripts\activate.bat  # activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Установите переменные окружения (environment variables)

Создайте файл `.env`. После скопируйте это в него

```dotenv
BOT_TOKEN=<your_token_for_tg_bot>
DB_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
API_BASE_URL=<your_api_url>
DEBUG=True
```
_**Не забудьте поменять значения на свои! (поставьте их после "=")**_

#### Больше о переменных:

BOT_TOKEN - токен telegram-бота<br>
DB_URL - url базы данных (не обязательно postgresql)<br>
API_BASE_URL - url API<br>
DEBUG - True/False, определяет логику логирования, в продакшене должен (must) быть False<br>

### 7. Запустите проект

Запустите файл main.py
