# Takehome Test (Full-Stack)

## Overview

This is a takehome test for candidates applying for a full-stack developer
position at Merkle Capital. It contains four sections: "Frontend", "Backend", "Databases" and "Follow-up" which
together include a series of tests involving HTML, CSS, JavaScript (TypeScript), Node.js and SQL.

Feel free to solve these questions however you see fit, using whatever coding
style or third-party libraries you think are appropriate.

To start the test, simply clone this repo and make your edits locally.

## Frontend

For the frontend portion of the test, use the `/frontend` folder. There are 5 features we'd like to add:

1. Fetch and display the list of symbols available on Blockchain API (see endpoint below).
2. Add CSS to create a responsive layout that will display one column on mobile
   devices, two columns on tablet devices, and three columns on desktops.
3. Add a toggle to control if symbols with status "open" should be only displayed.
4. Add a button to sort the list of symbols by alphabetical order using the "id" of the symbols.
5. Add a button to apply a random shuffle to the list of currencies when it is clicked.

Feel free to structure the code however you prefer and use third-party libraries at your discretion.

### API Information

- **Blockchain Symbols API `GET /v3/exchange/symbols` endpoint:** https://api.blockchain.com/v3/exchange/symbols

## Backend

For the backend portion of the test, use the `/backend` folder. We'd like to write some code that achieves the following:

1. Create a JSON API (REST or GraphQL) using Node.js which will return which cryptocurrency exchange we should use to buy a given amount of Bitcoin to minimise the amount of USD or USDT we'll spend on this trade.

Example API call (for 1 BTC):

```
curl http://localhost:4000/exchange-routing?amount=1
```

Example API response (if Coinbase price of \$10,000 / BTC is the cheapest):

```
{
  "btcAmount": 1,
  "usdAmount": 10000,
  "exchange": "coinbase"
}
```

1. You'll need to compare data from Binance and Coinbase Exchange and compute the best execution price for the given amount of Bitcoin we want to buy. (You can assume that 1 USDT = 1 USD at all time.)

Feel free to structure the code however you prefer and use third-party libraries at your discretion.

### API Information & Documentation

- **Binance API Documentation:** https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md
- **Coinbase Exchange API Documentation:** https://docs.cdp.coinbase.com

_Note that both APIs above are public and don't require any authentication._

## Databases

For the databases portion of the test, use the `/databases` folder.

Let's say you have two SQL tables: `users` and `transactions`.

The `users` dataset has 1M+ rows; here are the first three:
| id | email | country |
|--------|------------------|---------|
| user_1 | user1@merkle.capital | FRA |
| user_2 | user2@merkle.capital | GBR |
| user_3 | user3@merkle.capital | USA |

The `transactions` dataset has 1M+ rows; here are the first three:
| id | quote_currency | usd_amount | user_id |
|---------------|----------------|------------|---------|
| transaction_1 | btc | 100 | user_3 |
| transaction_2 | btc | 2000 | user_2 |
| transaction_3 | eth | 50 | user_1 |

1. Create a SQL query that shows the TOP 3 customers who spent the most.
2. Write an SQL query to find out how many users spent more than $1,000 but less than $2,000.
3. Print every country where the average lifetime spending per user is lower than \$500.

## Follow-up

Answer the questions in the [FOLLOW-UP.md](./FOLLOW-UP.md) file.

## Submitting Your Code

Once you've completed the test, please compress your files (via zip or tar) and
return them as a link or email attachment in reply to your test invite.

Once we receive it, a member of our team will review and we'll get back to you
as soon as possible.

Thanks!




# Frontend

สำหรับส่วนของ frontend คุณจะต้องทำตามข้อกำหนดดังนี้:

1. **Fetch และแสดงรายการ symbols จาก Blockchain API**:
   - คุณจะต้องใช้ JavaScript (หรือ TypeScript) เพื่อดึงข้อมูลจาก API `GET /v3/exchange/symbols` ของ Blockchain และแสดงผลในหน้าเว็บ

2. **เพิ่ม CSS เพื่อสร้าง layout ที่ responsive**:
   - ใช้ CSS เพื่อทำให้ layout ของหน้าเว็บสามารถแสดงผลได้ดีบนอุปกรณ์ต่าง ๆ โดยแสดงเป็นหนึ่งคอลัมน์บนมือถือ สองคอลัมน์บนแท็บเล็ต และสามคอลัมน์บนเดสก์ท็อป

3. **เพิ่ม toggle เพื่อควบคุมการแสดงผล symbols ที่มีสถานะ “open”**:
   - เพิ่มปุ่ม toggle ที่จะกรองรายการ symbols ให้แสดงเฉพาะ symbols ที่มีสถานะ “open”

4. **เพิ่มปุ่มเพื่อเรียงลำดับรายการ symbols ตามตัวอักษร**:
   - เพิ่มปุ่มที่เมื่อคลิกแล้วจะเรียงลำดับรายการ symbols ตามตัวอักษรโดยใช้ “id” ของ symbols

5. **เพิ่มปุ่มเพื่อสุ่มรายการ symbols**:
   - เพิ่มปุ่มที่เมื่อคลิกแล้วจะสุ่มเรียงลำดับรายการ symbols ใหม่

# Backend

สำหรับส่วนของ backend คุณจะต้องทำตามข้อกำหนดดังนี้:

1. **สร้าง JSON API (REST หรือ GraphQL) ด้วย Node.js**:
   - สร้าง API ที่จะคำนวณและส่งคืนข้อมูลว่าเราควรใช้ exchange ใดในการซื้อ Bitcoin เพื่อให้ใช้จ่าย USD หรือ USDT น้อยที่สุด

2. **เปรียบเทียบข้อมูลจาก Binance และ Coinbase Exchange**:
   - ดึงข้อมูลราคาจาก Binance และ Coinbase Exchange และคำนวณราคาที่ดีที่สุดสำหรับการซื้อ Bitcoin ตามจำนวนที่กำหนด

# Databases

สำหรับส่วนของ databases คุณจะต้องทำตามข้อกำหนดดังนี้:

1. **สร้าง SQL query เพื่อแสดงลูกค้าที่ใช้จ่ายมากที่สุด 3 อันดับแรก**:
   - เขียน SQL query ที่จะดึงข้อมูลลูกค้าที่ใช้จ่ายมากที่สุด 3 อันดับแรกจากตาราง `users` และ `transactions`

2. **เขียน SQL query เพื่อหาจำนวนผู้ใช้ที่ใช้จ่ายมากกว่า $1,000 แต่ไม่เกิน $2,000**:
   - เขียน SQL query ที่จะดึงข้อมูลจำนวนผู้ใช้ที่ใช้จ่ายในช่วง $1,000 ถึง $2,000

3. **แสดงประเทศที่มีการใช้จ่ายเฉลี่ยต่อผู้ใช้ต่ำกว่า $500**:
   - เขียน SQL query ที่จะดึงข้อมูลประเทศที่มีการใช้จ่ายเฉลี่ยต่อผู้ใช้ต่ำกว่า $500

# Follow-up

ในส่วนของ follow-up คุณจะต้องตอบคำถามในไฟล์ `FOLLOW-UP.md` ซึ่งจะมีคำถามเกี่ยวกับการออกแบบและการตัดสินใจที่คุณทำในโปรเจ็คนี้

ถ้าคุณมีคำถามเพิ่มเติมหรืออยากได้คำแนะนำเพิ่มเติมเกี่ยวกับการทำแต่ละส่วน บอกได้เลยนะครับ ผมยินดีช่วยเหลือ 😊
