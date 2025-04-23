import requests, json, datetime, time, pathlib

COINDESK = "https://api.coindesk.com/v1/bpi/currentprice.json"
COINGECKO = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
OUTFILE = pathlib.Path("btc_price.json")

def fetch_price():
    try:
        r = requests.get(COINDESK, timeout=(5, 20))
        r.raise_for_status()
        return r.json()["bpi"]["USD"]["rate_float"]
    except requests.exceptions.RequestException:
        # fallback
        r = requests.get(COINGECKO, timeout=(5, 20))
        r.raise_for_status()
        return r.json()["bitcoin"]["usd"]

def save(price):
    payload = {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "btc_usd": round(price, 2)
    }
    OUTFILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    for _ in range(3):          # tối đa 3 lần thử toàn bộ quá trình
        try:
            save(fetch_price())
            print("✅ Đã lưu giá BTC vào", OUTFILE)
            break
        except Exception as e:
            print("Thử lại do:", e)
            time.sleep(3)
