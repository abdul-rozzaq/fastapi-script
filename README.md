## O'rnatish

0. Virtual muhit yaratish:

linux va mac uchun

```bash
python3 -m venv venv && source venv/bin/activate
```

windows uchun

```bash
python -m venv venv
venv\Scripts\activate
```

1. Kerakli kutubxonalarni o'rnating:

```bash
pip install -r requirements.txt
```

2. `.env` fayl yarating va kerakli o'zgaruvchilarni qo'shing:

```bash
NGROK_AUTHTOKEN=authtoken
NGROK_URL=url #ngrok ishga tushganidan keyin o'zgartiriladi
```

3. `ngrok` ni ishga tushirish:

```bash
docker compose up
```

4. `.env` dagi `NGROK_URL` ni yangilash:

```bash
NGROK_URL=ngrok_url
```

## Ishga tushirish

Dasturni ishga tushirish uchun:

```bash
python main.py
```

Server `http://localhost:8000` manzilida ishga tushadi.

## Foydalanish

1. Dastur ishga tushgandan so'ng, terminal orqali xabar kiriting
2. Server POST so'rovlarni qabul qiladi
3. Natijalar konsolda ko'rsatiladi
