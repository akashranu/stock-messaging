import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = "ENTER TWILIO "
NEWS_API_KEY = "ENTER NEWS API KEY"
TWILIO_SID = "ENTER YOUR TWILIO SID"
TWILIO_AUTH_NUM = "ENTER TWILIO AUTHENTICATION NUMBER"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"] #putting this after the response is necessary so i can access that directory
data_list = [value for (key, value) in data.items()]
 #all data from day before, open, high, low, volume and close
closing_price = data_list[0]["4. close"]
closing_price_before_yesterday = data_list[1]["4. close"]


price_change = abs(float(closing_price) - float(closing_price_before_yesterday))
print(price_change)

up_down = None
if price_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percent_diff = (price_change / float(closing_price)) * 100
print(percent_diff)

news_params = {
        "apikey": NEWS_API_KEY,
        "qinTitle": COMPANY_NAME,

    }
news_response = requests.get(NEWS_ENDPOINT, params=news_params)
articles = news_response.json()["articles"]
three_articles = articles[:3]
formatted_articles = [f"{STOCK_NAME}: {up_down}{percent_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
print(articles)

client = Client(TWILIO_ID, TWILIO_AUTH_NUM)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_="+513230937",
        to= "077XXXXXXXXXX"
    )