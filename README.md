# 🔍 Wordstat API Web Interface

Веб-интерфейс для работы с [Yandex Wordstat API](https://yandex.ru/support2/wordstat/ru/content/api-wordstat).

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Возможности

- 📊 **Топ запросов** — популярные запросы по ключевой фразе + похожие запросы
- 📈 **Динамика** — график изменения частоты запросов по месяцам (Chart.js)
- 🗺️ **Регионы** — распределение запросов по городам России (~1000 регионов)
- 📉 **Квота** — отслеживание лимита API запросов

## 🖼️ Скриншот

Интерфейс включает:
- Поле ввода поисковой фразы
- Выбор региона
- Интерактивные графики
- Debug-консоль для отладки

## 🚀 Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/wordstat-api.git
cd wordstat-api
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте токен

Скопируйте `.env.example` в `.env` и добавьте свой OAuth-токен:

```bash
cp .env.example .env
nano .env
```

```
WORDSTAT_TOKEN=your_oauth_token_here
```

### 4. Запустите

```bash
python app.py
```

Откройте http://localhost:80 в браузере.

## 🔑 Получение OAuth-токена

1. Создайте приложение на [oauth.yandex.ru](https://oauth.yandex.ru/client/new)
2. Подайте заявку на доступ к Wordstat API в [документации](https://yandex.ru/support2/wordstat/ru/content/api-wordstat)
3. Дождитесь одобрения (~24 часа)
4. Получите токен по URL:
   ```
   https://oauth.yandex.ru/authorize?response_type=token&client_id=YOUR_CLIENT_ID
   ```

## 📁 Структура проекта

```
wordstat-api/
├── app.py              # Flask веб-приложение
├── wordstat_client.py  # Python-клиент для CLI
├── test_api.py         # Тестовый скрипт
├── requirements.txt    # Зависимости
├── .env.example        # Пример конфигурации
└── README.md
```

## 🔧 Systemd (для сервера)

Создайте `/etc/systemd/system/wordstat.service`:

```ini
[Unit]
Description=Wordstat API Web Interface
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/wordstat-api
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable wordstat
systemctl start wordstat
```

## 📊 API методы

| Метод | Описание |
|-------|----------|
| `/v1/topRequests` | Топ запросов по фразе |
| `/v1/dynamics` | Динамика по времени |
| `/v1/regions` | Распределение по регионам |
| `/v1/userInfo` | Информация о квоте |

## ⚡ Лимиты API

- 10 запросов в секунду
- 1024 запроса в сутки
- API бесплатный

## 📄 Лицензия

MIT License

## 🔗 Ссылки

- [Документация Wordstat API](https://yandex.ru/support2/wordstat/ru/content/api-wordstat)
- [Yandex OAuth](https://oauth.yandex.ru/)
- [Wordstat Web](https://wordstat.yandex.ru/)
