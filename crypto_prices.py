import requests
import pandas as pd
import streamlit as st


def get_data(currency_type, no_of_days, coin):
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={currency_type}&days={no_of_days}&interval=daily')
    response = response.json()['prices']
    df = pd.DataFrame(response, columns=['Date', 'Prices'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    df.set_index(df.Date, inplace=True)
    df.drop('Date', axis=1, inplace=True)
    return df


if __name__ == '__main__':
    st.title("Crypto Prices")
    days = st.slider('Days', min_value=1, max_value=365, value=90)
    coins = st.radio('Coins', ('bitcoin', 'ethereum'))
    currency = st.radio('Currency', ('USD', 'CAD', 'INR'))
    data = get_data(currency, days, coins)
    st.line_chart(data.Prices)
    st.write('Average price during this time was', sum(data['Prices']) / days)
