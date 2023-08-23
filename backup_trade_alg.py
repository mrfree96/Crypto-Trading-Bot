from binance.client import Client

import time
import math

# Calculates average price for last two minutes
def AvgPriceForThePriceList(priceList):
    total = sum(priceList)
    length = len(priceList)
    avg = total / length
    return avg

class BinanceConnection:

    def __init__(self, file):
        self.connect(file)

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

if __name__ == '__main__':
    filename = 'credientials.txt'
    connection = BinanceConnection(filename)

    #list of two minute price
    #last_ten_seconds_price = []
    last_two_minute_price = []

    symbol = 'BTCBUSD'
    interval = '5m'
    limit = 500
    while True:
        time.sleep(2) # its seconds
        try:
            klines = connection.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        except Exception as exp:
            print(exp.status_code, flush=True)
            print(exp.message, flush=True)

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]

        last_closing_price = close[-1]

        previous_closing_price = close[-2]

        print('Last closing price', last_closing_price, ', Previous closing price', previous_closing_price)
        balance_BTC = connection.client.get_asset_balance(asset='BTC')
        print("BTC Balance:", balance_BTC['free'])
        wallet_busd = float(connection.client.get_asset_balance(asset='BUSD')['free'])
        print("Wallet BUSD:", wallet_busd)
        #min_buy_price =  41000.0
        max_buy_price =  43000.0




        last_transaction = connection.client.get_my_trades(symbol=symbol)[-1]
        one_before_last_transaction = connection.client.get_my_trades(symbol=symbol)[-2]
        is_bought = False
        if one_before_last_transaction['isBuyer'] == True:
            bought_price = one_before_last_transaction['price']
            print("Last bought price: ", bought_price)
            is_bought = True
        elif last_transaction['isBuyer'] == True:
            bought_price = last_transaction['price']
            print("Last bought price: ", bought_price)
            is_bought = True


        stepSize = 0.0000100
        #profitPercentage = 0.0010
        #sell_price = float(bought_price) + (float(bought_price) * profitPercentage)
        if is_bought == True:
            sell_price = float(bought_price) + 150.0
            print("When BTC reaches this price, it will be sold: ", sell_price)

            # Adding current price to price list, calculating average and testing the buy
            if len(last_two_minute_price) < 60:
                last_two_minute_price.append(last_closing_price)
                avg_of_price_for_last_two_minutes = AvgPriceForThePriceList(last_two_minute_price)
            elif len(last_two_minute_price) == 60:
                if (float((avg_of_price_for_last_two_minutes - last_closing_price)) >= 65.0):
                    if wallet_busd > float(22):
                        amount_of_buy = round((busd_available_for_trade / float(last_closing_price)), 5)
                        amount_of_buy = float("%.8f" % (float(amount_of_buy)))
                        precision = 8
                        amount_str = "{:0.0{}f}".format(amount_of_buy, precision)
                        amount_of_buy = float(amount_str)
                        if float(last_closing_price) < max_buy_price:
                            buy_order = connection.client.order_market_buy(symbol=symbol, quantity=amount_of_buy)
                    # balance = float(balance_BTC['free']) * 0.98
                    print("Test Buying transaction is done.")
                    print("Buying price : ", last_closing_price)
                del last_two_minute_price[0]
                last_two_minute_price.append(last_closing_price)
                avg_of_price_for_last_two_minutes = AvgPriceForThePriceList(last_two_minute_price)

            print(last_two_minute_price)
            print("Average : ", avg_of_price_for_last_two_minutes)

        #print("LOT SIZE AND OTHER",connection.client.get_symbol_info("BTCBUSD")) # if you need you can use for debugging
        busd_available_for_trade = float(wallet_busd) * 0.999


        balance_available_for_trade = float(balance_BTC['free']) * 0.999
        balance_available_for_trade = round(balance_available_for_trade, 5)
        amount_of_sell_BTC = float("%.8f" % (float(balance_available_for_trade)))
        #amount_of_sell_BTC = float('{:8f}'.format((amount_of_sell_BTC)))
        print("Ready for selling BTC : ", amount_of_sell_BTC)
        if (balance_available_for_trade > stepSize):
            if float(last_closing_price) > sell_price:
                sell_order = connection.client.order_market_sell(symbol=symbol, quantity= amount_of_sell_BTC)