from fastapi import FastAPI, HTTPException
import requests
import httpx
import ssl
from sqlalchemy import create_engine, text
import certifi
# print(certifi.where())

app = FastAPI()
ssl_context = ssl.create_default_context(cafile=certifi.where())
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test_db"
engine = create_engine(DATABASE_URL)

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/spot?currency=USD"
POLYGON_API_URL = "https://api.polygon.io/v3/reference/exchanges?asset_class=stocks&apiKey=igaUIziqROMRbYfNPTNSea0Xf2iXERPY"

BASE_URL = "https://api.coinbase.com/v2"

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

@app.get("/currencies")
async def get_currencies():
    # async with httpx.AsyncClient(verify=certifi.where()) as client:
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{BASE_URL}/currencies")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching currencies")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/exchange-rates")
async def get_exchange_rates(currency: str):
    # async with httpx.AsyncClient(verify=certifi.where()) as client:
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{BASE_URL}/exchange-rates?currency={currency}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching currencies")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/best-price")
async def get_best_price(amount: float):
    prices = {}

    async with httpx.AsyncClient(verify=False) as client:
        try:
            # Fetch price from Binance
            binance_response = await client.get(BINANCE_API_URL)
            binance_response.raise_for_status()
            prices['Binance'] = float(binance_response.json()['price'])

            # Fetch price from Coinbase
            coinbase_response = await client.get(COINBASE_API_URL)
            coinbase_response.raise_for_status()
            prices['Coinbase'] = float(coinbase_response.json()['data']['amount'])

            # Fetch price from Polygon
            polygon_response = await client.get(POLYGON_API_URL)
            polygon_response.raise_for_status()
            polygon_data = polygon_response.json()
            if 'results' in polygon_data and isinstance(polygon_data['results'], list) and len(polygon_data['results']) > 0:
                prices['Polygon'] = float(polygon_data['results'][0].get('c', 0))  # ใช้ .get() เพื่อหลีกเลี่ยง KeyError
            else:
                raise HTTPException(status_code=500, detail="No results found from Polygon")

            # Compare prices
            best_exchange = min(prices, key=prices.get)
            best_price = prices[best_exchange] * amount

            return {
                "amount": amount,
                "best_exchange": best_exchange,
                "best_price": best_price
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching prices")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
