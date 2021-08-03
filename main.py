import BinanceGetHistoricalData
from datetime import datetime

if __name__ == '__main__':
    path = "Binance_BTCUSDT_minute.csv"
    BinanceGetHistoricalData.ReadCSVFile(path)

    #unix = int("1567970000000")/1000
    #print(datetime.utcfromtimestamp(unix).strftime('%Y.%m.%d'))
    #print(datetime.utcfromtimestamp(unix).strftime('%H:%M'))



