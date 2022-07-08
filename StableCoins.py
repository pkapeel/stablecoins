import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CoinGeckoAPI import gecko

import cufflinks as cf
import plotly.offline as pylo

def get_supply(coinID, start, end):
    data_json = gecko().get_market_chart_range(coinID, start, end)
    df1 = pd.DataFrame(data_json['prices'], columns=['Timestamp', 'Price'])
    df1.set_index('Timestamp', inplace=True)

    df2 = pd.DataFrame(data_json['market_caps'], columns=['Timestamp', 'Market Cap'])
    df2.set_index('Timestamp', inplace=True)

    df = df1.join(df2, how='outer')
    df['Supply'] = df['Market Cap'] / df['Price']

    return df['Supply']

startDate = '2019-10-01' # Change to actual desired start date.
                         # Subtract dayWeight from the start date.
                         # df.dropna() to remove NaN from data and graph.
endDate = '2022-07-03'

USDT_supply = get_supply('tether', startDate, endDate)
USDC_supply = get_supply('usd-coin', startDate, endDate)
BUSD_supply = get_supply('binance-usd', startDate, endDate)
USDP_supply = get_supply('paxos-standard', startDate, endDate)
TUSD_supply = get_supply('true-usd', startDate, endDate)

total_supply = pd.DataFrame({
                             'USDT Supply': USDT_supply, 
                             'USDC Supply': USDC_supply,
                             'BUSD Supply': BUSD_supply,
                             'USDP Supply': USDP_supply,
                             'TUSD Supply': TUSD_supply,
                             })

total_supply['Total Supply'] = total_supply.sum(axis=1, skipna=True)
total_supply.index = pd.to_datetime(total_supply.index, unit='ms')

dayWeight = 91
moving_average = total_supply.rolling(window=7).mean()
change = (((moving_average.pct_change(dayWeight) + 1) ** (365/dayWeight)) - 1) * 100 # Annualized Percentage Change.

pylo.iplot(
        change['Total Supply'].iplot(
                                    asFigure=True, 
                                    title='Growth Rate of Fiat-Backed Stablecoin Supply (7-Day Moving Average, 3-Month Change, Annualized)', 
                                    xTitle='Date', 
                                    yTitle='Annualized Percent Change', 
                                    color='blue',
                                    mode='lines+markers', 
                                    size=5.0,
                                    ), 
        image='png', 
        filename='ply_01',
        )


#plt.subplot(1, 1, 1)
#plt.plot(change)
#plt.legend()
#plt.show()


# Weekly Report
# Add attribution to coingecko
print(change.tail(7).round(2))

