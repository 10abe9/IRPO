from fastapi import FastAPI
import uvicorn
import requests
from config import api_key


app = FastAPI()


def get_exchange_rates(api_key):
    base_url = "https://openexchangerates.org/api/latest.json"
    params = {
        "app_id": api_key
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        rates = response.json()["rates"]
        return rates
    else:
        print("Ошибка при получении курса валют:", response.status_code)
        return None


exchange_rates = get_exchange_rates(api_key)
print(exchange_rates)


@app.get("/")
def get():
    return ({"Все курсы валют к доллару: ": exchange_rates})


@app.get("/calculate/{val}")
def calculate(value, name):
    course = exchange_rates[name]
    print(course)
    result = float(value)*float(course)
    return (f"{value} валюты {name} будет стоить {result} долларов")


if __name__ == '__main__':
    uvicorn.run(app)