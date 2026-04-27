# 📧 Automated-Emails

> A **scheduled news-digest mailer** that reads a list of recipients from Excel and sends each one personalized headlines from [NewsAPI.org](https://newsapi.org) every day at a fixed time.

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![NewsAPI](https://img.shields.io/badge/data-NewsAPI.org-orange)]()
[![Yagmail](https://img.shields.io/badge/email-yagmail-red)]()
[![Pandas](https://img.shields.io/badge/excel-pandas-yellow)]()

---

## 📌 Overview

A small automation project that ties together three useful skills:

1. **Reading structured data from Excel** with `pandas`
2. **Calling a public REST API** (NewsAPI.org) and parsing the JSON
3. **Sending Gmail emails programmatically** via `yagmail`

The script runs in an infinite loop and, **at a configured time of day**, iterates through every row of `people.xlsx`, fetches yesterday's news matching that person's `interest`, and emails them a digest.

> 💡 Tip from the original notes: free disposable test inboxes are available at [dropmail.me](https://dropmail.me) — handy when iterating without spamming real addresses.

## 🧱 Architecture

```
                   ┌──────────────┐
                   │ people.xlsx  │
                   │ name|email|  │
                   │ interest     │
                   └──────┬───────┘
                          │
              pandas reads each row
                          │
                          ▼
   ┌──────────────────────────────────────────┐
   │  for each person at HH:MM each day:      │
   │                                          │
   │  ┌──────────────┐    ┌────────────────┐  │
   │  │ NewsFeed     │───▶│ NewsAPI.org    │  │
   │  │ (interest,   │    │ /v2/everything │  │
   │  │  date range) │◀───│ JSON response  │  │
   │  └──────┬───────┘    └────────────────┘  │
   │         │  email_body = title + url ...  │
   │         ▼                                │
   │  ┌─────────────────────┐                 │
   │  │ yagmail.SMTP.send() │ ─▶ Gmail        │
   │  └─────────────────────┘                 │
   └──────────────────────────────────────────┘
```

## 🗂️ Project Structure

```
Automated-Emails/
├── main.py            # Scheduler loop + email composition
├── news.py            # NewsFeed class — wraps NewsAPI.org
├── people.xlsx        # Recipient list (name, email, interest)
├── design.txt         # Notes / attached to the email body
└── requirements.txt
```

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure credentials

You need:
- A **NewsAPI.org** API key — [register here](https://newsapi.org/register)
- A **Gmail App Password** — [generate one](https://support.google.com/accounts/answer/185833) (regular passwords won't work with `yagmail`)

Then edit:

**`news.py`**
```python
api_key = 'YOUR_NEWSAPI_KEY'
```

**`main.py`**
```python
email = yagmail.SMTP(user="your_email@gmail.com", password="your_gmail_app_password")
```

### 3. Prepare the recipient list

Create `people.xlsx` with the columns:

| name  | email           | interest  |
|-------|-----------------|-----------|
| Alice | alice@mail.com  | bitcoin   |
| Bob   | bob@mail.com    | football  |
| Carla | carla@mail.com  | python    |

### 4. Configure the send time

In `main.py`, adjust the schedule:
```python
if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 33:
    ...
```

### 5. Run
```bash
python main.py
```
Leave the script running on a server / VM / Raspberry Pi to keep the daily loop alive.

## 🧩 Core Class — `NewsFeed`

```python
NewsFeed(interest='bitcoin', from_date='2023-01-01', to_date='2023-01-02', language='en').get()
```

Calls the NewsAPI `/v2/everything` endpoint:
- Query: `qInTitle` filter on the interest term
- Date range: `from` / `to`
- Sorted by `publishedAt` descending
- Language filter (default `en`)

Returns a plain text body of `title + URL` pairs, ready to drop into an email.

## ⚠️ Notes & Gotchas

- The `while True: ... time.sleep(60)` loop polls every minute — fine for a single dispatch per day, but for production prefer **cron** or **APScheduler**.
- NewsAPI's free tier is **rate-limited** to 100 requests/day and only returns articles up to **24h old**.
- Gmail's daily send limit is **500 messages/day** for free accounts.

## 💡 Possible Extensions

- HTML emails (yagmail supports `contents=html`)
- Replace the polling loop with **cron** or **APScheduler**
- Store the recipient list in a DB instead of `.xlsx`
- Track open/click rates via UTM tags
- Containerize with Docker and deploy to a cheap VPS

## 👤 Author

**Denis Vreshtazi** — [GitHub](https://github.com/denisvreshtazi)
