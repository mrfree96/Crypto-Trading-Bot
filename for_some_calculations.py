"""
This file for some basic calculations to create logic for trading bot..
"""


from datetime import datetime

# fake coin price to test
coin_price = 43895.0

# fake busd amount to test
busd = 155.37295
# available busd for trading
busd_available_for_trade = busd * 0.999

# balance calculation and rounding
balance = round((busd_available_for_trade / coin_price) , 5)
print("Wallet Coin Amount : ", balance)

# for selling
last_btc_price = coin_price + 150.0


step_size = 0.00001

balance_available_for_trade = balance * 0.999
#balance_available_for_trade = round(balance_available_for_trade, 7)
busd_after_selling =  round(balance_available_for_trade,5) * last_btc_price
profit = busd_after_selling - busd
print("Selling price : ", busd_after_selling)
print("Profit :", profit)

#print(format(float('1.72e-05'), 'f'))
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)



