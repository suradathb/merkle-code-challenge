from fastapi import FastAPI, HTTPException
import requests
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:rootpassword@db/test_db"
engine = create_engine(DATABASE_URL)

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/spot?currency=USD"

@app.get("/exchange-routing")
def get_best_exchange(amount: float):
    try:
        # Fetch price from Binance
        binance_response = requests.get(BINANCE_API_URL, verify=False)
        binance_response.raise_for_status()
        binance_data = binance_response.json()
        binance_price = float(binance_data['price'])

        # Fetch price from Coinbase
        coinbase_response = requests.get(COINBASE_API_URL, verify=False)
        coinbase_response.raise_for_status()
        coinbase_data = coinbase_response.json()
        coinbase_price = float(coinbase_data['data']['amount'])

        # Calculate the total cost for the given amount of BTC
        binance_total = amount * binance_price
        coinbase_total = amount * coinbase_price

        # Determine the best exchange
        if binance_total < coinbase_total:
            best_exchange = "binance"
            best_price = binance_total
        else:
            best_exchange = "coinbase"
            best_price = coinbase_total

        return {
            "btcAmount": amount,
            "usdAmount": best_price,
            "exchange": best_exchange
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top-spenders")
def get_top_spenders():
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT user_id, SUM(usd_amount) AS total_spent
            FROM transactions
            GROUP BY user_id
            ORDER BY total_spent DESC
            LIMIT 3;
        """))
        return [dict(row) for row in result]

@app.get("/spenders-range")
def get_spenders_range():
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT COUNT(*)
            FROM (
                SELECT user_id, SUM(usd_amount) AS total_spent
                FROM transactions
                GROUP BY user_id
                HAVING total_spent > 1000 AND total_spent < 2000
            ) AS subquery;
        """))
        return {"count": result.scalar()}

@app.get("/countries-low-spending")
def get_countries_low_spending():
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT country
            FROM users
            JOIN (
                SELECT user_id, AVG(usd_amount) AS avg_spent
                FROM transactions
                GROUP BY user_id
            ) AS user_spending ON users.id = user_spending.user_id
            GROUP BY country
            HAVING AVG(user_spending.avg_spent) < 500;
        """))
        return [dict(row) for row in result]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
