# Деплой на drobitko.pro

## Инфраструктура

- **Сервер:** Ubuntu 24.04 на FirstVDS (92.63.103.97)
- **Домен:** drobitko.pro (DNS на nic.ru)
- **Веб-сервер:** nginx (reverse proxy)
- **Backend:** Flask на Python 3.12
- **SSL:** Let's Encrypt (автопродление)

## Архитектура

```
Интернет → nginx (0.0.0.0:80/443) → Flask (127.0.0.1:5000)
```

## Настройка с нуля

### 1. Flask
```bash
cd /root/wordstat-api
# app.py слушает 127.0.0.1:5000
python3 app.py
```

### 2. nginx
```bash
# Создать конфиг
nano /etc/nginx/sites-available/drobitko.pro

# Включить сайт
ln -s /etc/nginx/sites-available/drobitko.pro /etc/nginx/sites-enabled/

# Проверить конфиг
nginx -t

# Перезапустить
systemctl restart nginx
```

### 3. SSL (Let's Encrypt)
```bash
certbot --nginx -d drobitko.pro -d www.drobitko.pro
```

Сертификат обновляется автоматически через systemd timer.

## DNS на nic.ru

Записи типа A:
- `@` → 92.63.103.97
- `www` → 92.63.103.97

## Systemd сервис

```bash
# Статус
systemctl status wordstat.service

# Перезапуск
systemctl restart wordstat.service

# Логи
journalctl -u wordstat.service -f
```

## Проверка работы

```bash
# HTTP → HTTPS редирект
curl -I http://drobitko.pro

# HTTPS работает
curl -I https://drobitko.pro

# Flask отвечает
curl http://127.0.0.1:5000/
```

## Обновление кода

```bash
cd /root/wordstat-api
git pull
systemctl restart wordstat.service
```
