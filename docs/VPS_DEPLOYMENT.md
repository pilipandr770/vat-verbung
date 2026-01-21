# VPS Deployment Guide

## Почему VPS?

❌ **Render (Cloud)** - IP в черном списке Instagram
✅ **VPS с Residential IP** - не блокируется, полный контроль

---

## Выбор VPS провайдера

### Рекомендуемые провайдеры с Residential IP:

| Провайдер | IP Type | Цена | Особенности |
|-----------|---------|------|------------|
| **Hetzner** | Dedicated | €3-5/мес | Мощный, надежный, Германия |
| **DigitalOcean** | Standard | $5/мес | Простой, хороший апtime |
| **Linode** | Standard | $5/мес | Быстрый, аналитика |
| **Contabo** | Residential | €3/мес | Жилой IP, дешево |
| **OVH** | Standard | €3-5/мес | Европа, мощный |

**Лучший выбор для проекта:**
- **Hetzner CX22** (~€5/мес) - 2 ядра, 4GB RAM, 40GB SSD
- или **DigitalOcean Basic** ($5/мес) - 1 ядро, 1GB RAM, 25GB SSD

---

## Step 1: Создание VPS на Hetzner

### 1.1 Регистрация
1. Перейти https://www.hetzner.com/cloud
2. Создать аккаунт
3. Добавить способ оплаты

### 1.2 Создание сервера
1. Cloud Console → Servers → Create Server
2. Выбрать регион: **Frankfurt** (ближайший к EU)
3. Выбрать ОС: **Ubuntu 22.04 LTS**
4. Выбрать тип: **CX22** (~€5/мес)
5. SSH Key: добавить ваш публичный ключ (или взять временный пароль)
6. Create Server

### 1.3 Получить IP адрес
- В консоли появится IPv4 адрес (например: `123.45.67.89`)

---

## Step 2: Первоначальная настройка VPS

### 2.1 Подключиться к серверу
```bash
ssh root@123.45.67.89
# или если используете пароль:
# ssh -o StrictHostKeyChecking=no root@123.45.67.89
```

### 2.2 Обновить систему
```bash
apt update && apt upgrade -y
```

### 2.3 Установить зависимости
```bash
# Python, Git, PostgreSQL client
apt install -y python3.13 python3-pip git postgresql-client curl wget

# Проверить Python версию
python3 --version
```

### 2.4 Создать пользователя (не root)
```bash
adduser promotion
# Задать пароль, можно пропустить доп. поля (Enter x5)

# Добавить в sudoers
usermod -aG sudo promotion

# Переключиться на пользователя
su - promotion
```

---

## Step 3: Развёртывание проекта

### 3.1 Клонировать репозиторий
```bash
cd /home/promotion
git clone https://github.com/pilipandr770/vat-verbung.git
cd vat-verbung/promotion_hub
```

### 3.2 Создать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Установить зависимости
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.4 Настроить .env
```bash
# Скопировать шаблон
cp .env.example .env

# Отредактировать (использовать nano или vim)
nano .env
```

**Необходимые переменные:**
```bash
# Database (PostgreSQL на Render или другой хост)
DATABASE_URL=postgresql://user:password@host:5432/dbname
DB_SCHEMA=promotion_hub

# Social Media
LINKEDIN_USERNAME=your@email.com
LINKEDIN_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
INSTAGRAM_USERNAME=your_instagram_email
INSTAGRAM_PASSWORD=your_instagram_password

# AI
OPENAI_API_KEY=sk-...your_key...

# Other
LOG_LEVEL=INFO
```

### 3.5 Тестировать локально
```bash
python main.py
# Должен запуститься без ошибок
# Ctrl+C для остановки
```

---

## Step 4: Systemd Service (автозапуск)

### 4.1 Создать service file
```bash
sudo nano /etc/systemd/system/promotion-hub.service
```

### 4.2 Вставить конфиг
```ini
[Unit]
Description=Promotion Hub - B2B Marketing Automation
After=network.target

[Service]
Type=simple
User=promotion
WorkingDirectory=/home/promotion/vat-verbung/promotion_hub
Environment="PATH=/home/promotion/vat-verbung/promotion_hub/venv/bin"
ExecStart=/home/promotion/vat-verbung/promotion_hub/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 4.3 Включить и запустить
```bash
sudo systemctl daemon-reload
sudo systemctl enable promotion-hub
sudo systemctl start promotion-hub

# Проверить статус
sudo systemctl status promotion-hub

# Смотреть логи
sudo journalctl -u promotion-hub -f
```

---

## Step 5: Nginx (опционально, для HTTP API)

Если нужен web interface или health check на порту 80:

### 5.1 Установить Nginx
```bash
sudo apt install -y nginx
```

### 5.2 Создать конфиг
```bash
sudo nano /etc/nginx/sites-available/promotion-hub
```

### 5.3 Вставить конфиг
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5.4 Включить и перезагрузить
```bash
sudo ln -s /etc/nginx/sites-available/promotion-hub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 6: Мониторинг и логи

### Просмотр логов
```bash
# Systemd логи
sudo journalctl -u promotion-hub -f

# Приложение логи
tail -f logs/promotion_hub.log
```

### Мониторинг процесса
```bash
# Проверить что работает
ps aux | grep python

# Проверить порт 5000
netstat -tuln | grep 5000

# Проверить health check
curl http://localhost:5000/health
```

---

## Step 7: Автоматические обновления кода

### 7.1 Deploy script
```bash
# Создать /home/promotion/deploy.sh
#!/bin/bash
cd /home/promotion/vat-verbung/promotion_hub
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart promotion-hub
```

### 7.2 Git webhook (опционально)
- Настроить webhook на GitHub
- При push → автоматический deploy на VPS

---

## Step 8: Резервная копия БД

### Ежедневный бэкап
```bash
# Создать скрипт /home/promotion/backup.sh
#!/bin/bash
pg_dump -U user dbname | gzip > /backups/db_$(date +%Y%m%d).sql.gz

# Добавить в crontab
crontab -e
# Добавить строку:
# 0 3 * * * /home/promotion/backup.sh
```

---

## Результат

Вы получите:
- ✅ **Жилой IP** - без блокировки Instagram
- ✅ **24/7 работа** - сервер всегда включен
- ✅ **Полный контроль** - root доступ, можно что угодно менять
- ✅ **Дешево** - €3-5 в месяц
- ✅ **Масштабируемо** - можно добавить больше ресурсов

---

## Troubleshooting

**Проблема: Service не запускается**
```bash
sudo journalctl -u promotion-hub -n 50  # Последние 50 строк логов
```

**Проблема: Instagram все еще блокирует**
```bash
# Проверить IP
curl https://api.ipify.org
# Если это shared IP - попросить residential IP у провайдера
```

**Проблема: БД не подключается**
```bash
# Проверить подключение
psql postgresql://user:password@host:5432/dbname -c "SELECT 1"
```

---

## References

- https://docs.hetzner.cloud/
- https://www.digitalocean.com/docs/droplets/
- https://www.linode.com/docs/

