import random
import time

"""
This python file exists for only testing some algorithms...
"""

# Function to calculate avg price of las two minute
def AvgPriceForTwoMinute(priceList):
    """
    This function calculates the Avg price of the last two minute..
    """
    total = sum(priceList)
    length = len(priceList)
    avg = total / length
    return avg

# list for one minute price
btc_one_minute_price_list = []

# list for last two minute price
last_two_minute_price = []

# for testing purpose creating fake data
# 121 data creating for simulation
for i in range(0, 1200):
    num = random.randint(42000, 43000)
    btc_one_minute_price_list.append(num)

print(len(btc_one_minute_price_list))

for i in range(0, 1200):
    anlık_fiyat = btc_one_minute_price_list[i]
    print("Anlık BTC fiyatı: ", anlık_fiyat)
    if len(last_two_minute_price) < 120:
        last_two_minute_price.append(anlık_fiyat)
        print(last_two_minute_price)
    elif len(last_two_minute_price) == 120:
        avg_of_price_for_two_minutes = AvgPriceForTwoMinute(last_two_minute_price)
        if (float((avg_of_price_for_two_minutes -  anlık_fiyat)) >= 200.0):
            print("Alış yapıldı.")
            print("Alış fiyatı : ", anlık_fiyat)
            print("Ortalama : ", avg_of_price_for_two_minutes)
            break
        del last_two_minute_price[0]
        last_two_minute_price.append(anlık_fiyat)
        print(last_two_minute_price)
    #time.sleep(1)