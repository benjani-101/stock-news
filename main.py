import os
import requests
from config import STOCK_PRICE_API_KEY, NEWS_API_KEY, TW_AUTH_TOKEN, TW_ACCOUNT_SID, TW_PHONE_NUMBER
from twilio_sms import sms_message

STOCK = "LON:BA.L"
COMPANY_NAME = "BAE Systems PLC"
STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://gnews.io/api/v4/search"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "GLOBAL_QUOTE",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": STOCK_PRICE_API_KEY
}

response = requests.get(url=STOCK_URL, params=stock_params)
response.raise_for_status()
stock_data = response.json()
print(stock_data)
yday_open_price = float(stock_data['Global Quote']['02. open'])
prev_close_price = float(stock_data['Global Quote']['08. previous close'])
change_pcnt = (yday_open_price - prev_close_price) / prev_close_price
print(change_pcnt)
if change_pcnt > 0.05 or change_pcnt < -0.05:
    print("Getting News")
    latest_trading_date = stock_data['Global Quote']["07. latest trading day"]

    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_params = {
        'q': COMPANY_NAME,
        'lang': 'en',
        'max': 3,
        'earliest-publish-date': latest_trading_date,
        'apikey': NEWS_API_KEY,
    }

    response = requests.get(url=NEWS_URL, params=news_params)
    response.raise_for_status()
    news_data = response.json()
    print(news_data)
    if change_pcnt > 0.05:
        indicator = "🔺"
    else:
        indicator = "🔻"
    message = f"{COMPANY_NAME}: {indicator} {(round(abs(change_pcnt * 100), 2))}%\n"
    for article in news_data['articles']:
        title = article['title']
        brief = article['description']
        if len(brief) > 200:
            brief = brief[:200] + "..."
        message += f"Headline: {title}\n" \
                   f"Brief: {brief}\n\n"
    sms_message(account_sid=TW_ACCOUNT_SID, auth_token=TW_AUTH_TOKEN,
                message=message, to_number="07906551409")



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

