## سرویس systemd برای ربات Aiogram
```
sudo nano /etc/systemd/system/bot1.service
```

```
[Unit]
Description=Telegram Bot (too_tele_bot)
After=network.target

[Service]
User=root
WorkingDirectory=/root/telebot/too_tele_bot
ExecStart=/root/telebot/too_tele_bot/venv/bin/python3 /root/telebot/too_tele_bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload       # لود تنظیمات جدید
sudo systemctl enable bot1         # اجرا بشه بعد از هر ریبوت
sudo systemctl start bot1          # همین الان ربات رو اجرا کن
sudo systemctl status bot1         # وضعیت ربات رو ببین
```

### لاگ‌ها هم به راحتی با دستور می‌گیری:

```
journalctl -u bot1 -f
```


