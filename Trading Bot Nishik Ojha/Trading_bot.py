# trading_bot.py

import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Setup Logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret, testnet=testnet)

        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
        logging.info("Initialized Binance Futures Client in {} mode".format("Testnet" if testnet else "Live"))

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info(f"Market Order Placed: {order}")
            print("✔ Market order placed successfully:", order)
            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API Exception (Market Order): {e}")
            print("❌ Binance API error:", e)
        except Exception as e:
            logging.error(f"General Exception (Market Order): {e}")
            print("❌ An error occurred:", e)

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            logging.info(f"Limit Order Placed: {order}")
            print("✔ Limit order placed successfully:", order)
            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API Exception (Limit Order): {e}")
            print("❌ Binance API error:", e)
        except Exception as e:
            logging.error(f"General Exception (Limit Order): {e}")
            print("❌ An error occurred:", e)

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                type=ORDER_TYPE_STOP_MARKET,
                stopPrice=stop_price,
                quantity=quantity,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logging.info(f"Stop-Market Order Placed: {order}")
            print("✔ Stop-Market order placed successfully:", order)
            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API Exception (Stop-Market Order): {e}")
            print("❌ Binance API error:", e)
        except Exception as e:
            logging.error(f"General Exception (Stop-Market Order): {e}")
            print("❌ An error occurred:", e)

# CLI Interface
if __name__ == '__main__':
    print("\n=== Binance Futures Trading Bot ===\n")
    api_key = input("Enter your Binance Testnet API Key: ").strip()
    api_secret = input("Enter your Binance Testnet Secret Key: ").strip()

    bot = BasicBot(api_key, api_secret, testnet=True)

    while True:
        symbol = input("Enter trading pair (e.g., BTCUSDT): ").upper()
        side = input("Order side (BUY/SELL): ").upper()
        order_type = input("Order type (MARKET / LIMIT / STOP_LIMIT): ").upper()
        quantity = float(input("Enter quantity: "))

        if order_type == 'MARKET':
            bot.place_market_order(symbol, side, quantity)

        elif order_type == 'LIMIT':
            price = input("Enter limit price: ")
            bot.place_limit_order(symbol, side, quantity, price)

        elif order_type == 'STOP_LIMIT':
            stop_price = input("Enter stop price: ")
            bot.place_stop_limit_order(symbol, side, quantity, stop_price, stop_price)

        else:
            print("❌ Invalid order type!")

        cont = input("\nDo you want to place another order? (y/n): ").lower()
        if cont != 'y':
            print("\n👋 Exiting bot. Goodbye!")
            break
