# 🚀 Быстрый старт на VPS

**За 10 минут сервер работает без блокировок!**

---

## 1️⃣ Арендовать VPS (2 минуты)

### Вариант A: Hetzner (€5/мес)
```bash
1. Перейти https://www.hetzner.com/cloud
2. Выбрать: Frankfurt, Ubuntu 22.04 LTS, CX22
3. Получить IP адрес: 123.45.67.89
```

### Вариант B: DigitalOcean ($5/мес)
```bash
1. Перейти https://www.digitalocean.com
2. Create Droplet: Ubuntu 22.04, Basic, Frankfurt
3. Получить IP адрес
```

---

## 2️⃣ SSH подключение (30 секунд)

```bash
ssh root@YOUR_IP_ADDRESS

# Если просит пароль - используйте полученный от провайдера
# или добавьте SSH key в консоль
```

---

## 3️⃣ Установка (5 минут)

Скопируйте и выполните:

```bash
#!/bin/bash
# Обновить систему
apt update && apt upgrade -y

# Установить зависимости
apt install -y python3.13 python3-pip git postgresql-client

# Создать пользователя
adduser --disabled-password --gecos "" promotion
usermod -aG sudo promotion

# Клонировать проект
su - promotion -c "
  cd ~
  git clone https://github.com/pilipandr770/vat-verbung.git
  cd vat-verbung/promotion_hub
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
"

# Создать .env
su - promotion -c "
  cd ~/vat-verbung/promotion_hub
  cp .env.example .env
  echo '⚠️ Edit .env with your credentials!'
"
```

---

## 4️⃣ Конфигурация .env (2 минуты)

```bash
sudo -u promotion nano ~/vat-verbung/promotion_hub/.env
```

Заполнить:
```bash
DATABASE_URL=postgresql://user:password@your-db-host:5432/your_db
LINKEDIN_USERNAME=your@email.com
LINKEDIN_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
INSTAGRAM_USERNAME=instagram_email
INSTAGRAM_PASSWORD=instagram_password
OPENAI_API_KEY=sk-...your_key...
LOG_LEVEL=INFO
```

---

## 5️⃣ Systemd Service (автозапуск) (2 минуты)

```bash
sudo tee /etc/systemd/system/promotion-hub.service > /dev/null <<EOF
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
EOF

# Запустить сервис
sudo systemctl daemon-reload
sudo systemctl enable promotion-hub
sudo systemctl start promotion-hub

# Проверить статус
sudo systemctl status promotion-hub
```

---

## 6️⃣ Проверка работы (30 секунд)

```bash
# Просмотреть логи (Ctrl+C для выхода)
sudo journalctl -u promotion-hub -f

# Должны быть строки типа:
# [OK] Health check started on port 5000
# [OK] Database initialized
# [OK] All systems ready!
# Scheduler started
```

---

## ✅ Готово!

Ваша система работает:
- ✅ **LinkedIn** - 2 поста в день
- ✅ **Telegram** - 5 постов в день  
- ✅ **Instagram** - 3 поста в день (БЕЗ блокировок!)
- ✅ **Сбор лидов** - каждые 6-8 часов
- ✅ **Auto-invites** - каждые 2-3 часа
- ✅ **24/7 работа** - автоматический перезапуск

---

## 📊 Мониторинг

```bash
# Проверить что работает
sudo systemctl status promotion-hub

# Смотреть логи в реальном времени
sudo journalctl -u promotion-hub -f

# Проверить health check
curl http://localhost:5000/health

# Проверить собрано постов
# Через БД или мониторинг
```

---

## 🔄 Обновления

```bash
# Получить новые версии из GitHub
su - promotion -c "
  cd ~/vat-verbung/promotion_hub
  git pull origin main
  source venv/bin/activate
  pip install -r requirements.txt
"

# Перезагрузить сервис
sudo systemctl restart promotion-hub
```

---

## 🆘 Проблемы?

**Сервис не запускается**
```bash
sudo journalctl -u promotion-hub -n 30
# Посмотреть последние 30 строк логов
```

**Instagram все ещё блокирует**
```bash
# Проверить IP
curl https://api.ipify.org
# IP должен быть от вашего VPS провайдера
# Если всё ещё блокирует - попросить residential IP у провайдера
```

**БД не подключается**
```bash
# Проверить соединение
psql "postgresql://user:password@host:5432/dbname"
```

---

## 📚 Полная документация

Смотри [VPS_DEPLOYMENT.md](VPS_DEPLOYMENT.md) для расширенной конфигурации.

---

**Готово!** 🎉 Система работает на вашем собственном сервере без ограничений Render!
