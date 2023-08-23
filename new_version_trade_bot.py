from binance.client import Client
import time
import math
from datetime import datetime

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

    # list of two minute price
    last_two_minute_price = []

    symbol = 'BTCBUSD'
    interval = '5m'
    limit = 500
    while True:
        time.sleep(1) # its seconds
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

        # getting time info
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        print("-----------------------------------------------------------------------------------------------")
        print('Last closing price', last_closing_price, ', previous closing price', previous_closing_price, "Time : ", current_time)
        balance_BTC = connection.client.get_asset_balance(asset='BTC')
        print("BTC Balance:", balance_BTC['free'])
        wallet_busd = float(connection.client.get_asset_balance(asset='BUSD')['free'])
        print("Wallet BUSD:", wallet_busd)
        # min_buy_price =  41000.0

        # incrementing setting..
        # This a bad logic to buy, you can implement your own logic..
        amount_of_increase = 150.0
        max_buy_price =  44800.0 - (amount_of_increase * 2)


        last_transaction = connection.client.get_my_trades(symbol=symbol)[-1]
        one_before_last_transaction = connection.client.get_my_trades(symbol=symbol)[-2]
        is_bought = False
        if last_transaction['isBuyer'] == True:
            bought_price = last_transaction['price']
            print("Last bought price: ", bought_price)
            is_bought = True
        elif one_before_last_transaction['isBuyer'] == True:
            bought_price = one_before_last_transaction['price']
            print("Last bought price: ", bought_price)
            is_bought = True

        stepSize = 0.0000100
        #profitPercentage = 0.0010
        #sell_price = float(bought_price) + (float(bought_price) * profitPercentage)
        if is_bought == True:
            sell_price = float(bought_price) + amount_of_increase
            print("When BTC reaches this price, it will be sold: ", sell_price)
            # Adding current price to price list, calculating average and testing the buy
            if len(last_two_minute_price) < 60:
                last_two_minute_price.append(last_closing_price)
                avg_of_price_for_last_two_minutes = AvgPriceForThePriceList(last_two_minute_price)
            elif len(last_two_minute_price) == 60:
                if (float((avg_of_price_for_last_two_minutes - last_closing_price)) >= 50.0):
                    if wallet_busd > float(22):
                        busd_available_for_trade = float(wallet_busd) * 0.999
                        amount_of_buy = round((busd_available_for_trade / float(last_closing_price)), 5)
                        amount_of_buy = float("%.8f" % (float(amount_of_buy)))
                        precision = 8
                        amount_str = "{:0.0{}f}".format(amount_of_buy, precision)
                        amount_of_buy = float(amount_str)
                        if float(last_closing_price) < max_buy_price:
                            buy_order = connection.client.order_market_buy(symbol=symbol, quantity=amount_of_buy)
                            print("Real buying transaction is done...")
                    # balance = float(balance_BTC['free']) * 0.98
                    print("Test Buying transaction is done.")
                    print("Buying price : ", last_closing_price)
                del last_two_minute_price[0]
                last_two_minute_price.append(last_closing_price)
                avg_of_price_for_last_two_minutes = AvgPriceForThePriceList(last_two_minute_price)

            print(last_two_minute_price)
            print("Average : ", avg_of_price_for_last_two_minutes)

        #print("LOT SIZE AND OTHER",connection.client.get_symbol_info("BTCBUSD")) # if you need you can use for debugging


        balance_available_for_trade = float(balance_BTC['free']) * 0.999
        balance_available_for_trade = round(balance_available_for_trade, 5)
        amount_of_sell_BTC = balance_available_for_trade
        #amount_of_sell_BTC = float("%.8f" % (float(balance_available_for_trade)))
        amount_of_sell_BTC = float(format(float(str(amount_of_sell_BTC)), 'f'))
        print("Ready for selling BTC : ", format(float(str(amount_of_sell_BTC)), 'f'))
        if (balance_available_for_trade > (stepSize*2)):
            if float(last_closing_price) > sell_price:
                sell_order = connection.client.order_market_sell(symbol=symbol, quantity= amount_of_sell_BTC)

    # #all symbols can get with the below codes
    # dict = connection.client.get_all_tickers()
    # #print(dict)
    # symbol_list = []
    # sub_str = 'DOGE'
    # for element in dict:
    #     symbol_list.append(element['symbol'])
    # for element in symbol_list:
    #     if sub_str in element:
    #         print(element)
    #buy_order = connection.client.order_market_buy(symbol=symbol, quantity=1)