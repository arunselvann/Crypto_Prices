import requests
from pandas import DataFrame, to_datetime
import streamlit as st


def get_data(currency_type: str, no_of_days: int, coin: str) -> DataFrame:
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={currency_type}'
                            f'&days={no_of_days}&interval=daily')
    response = response.json()['prices']
    df = DataFrame(response, columns=['Date', currency_type])
    df['Date'] = to_datetime(df['Date'], unit='ms')
    df.set_index(df.Date, inplace=True)
    df.drop('Date', axis=1, inplace=True)
    return df


if __name__ == '__main__':
    st.title("Crypto Prices")
    days = st.slider('Days', min_value=1, max_value=365, value=90)
    coins = st.radio('Coins', ('bitcoin', 'ethereum'))
    currency = st.radio('Currency', ('CAD', 'USD', 'INR'))
    data = get_data(currency, days, coins)
    st.line_chart(data[currency])
    st.write('Average price during this time was', sum(data[currency]) / days)
