import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
import sys

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        logging.info("Bot initialized with testnet: %s", testnet)

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logging.info("Market Order placed: %s", order)
            return order
        except BinanceAPIException as e:
            logging.error("Error placing market order: %s", e.message)
            print("Failed to place market order:", e.message)

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logging.info("Limit Order placed: %s", order)
            return order
        except BinanceAPIException as e:
            logging.error("Error placing limit order: %s", e.message)
            print("Failed to place limit order:", e.message)

    def get_order_status(self, symbol, order_id):
        try:
            status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logging.info("Fetched order status: %s", status)
            return status
        except BinanceAPIException as e:
            logging.error("Error fetching order status: %s", e.message)
            print("Failed to fetch order status:", e.message)

    def run_cli(self):
        print("\nWelcome to Binance Futures Bot")
        while True:
            try:
                print("\nOptions:\n1: Market Order\n2: Limit Order\n3: Order Status\n4: Exit")
                choice = input("Select option: ")

                if choice == '1':
                    symbol = input("Symbol (e.g., BTCUSDT): ")
                    side = input("Side (BUY/SELL): ").upper()
                    qty = float(input("Quantity: "))
                    result = self.place_market_order(symbol, side, qty)
                    print("Market Order Result:", result)

                elif choice == '2':
                    symbol = input("Symbol (e.g., BTCUSDT): ")
                    side = input("Side (BUY/SELL): ").upper()
                    qty = float(input("Quantity: "))
                    price = float(input("Price: "))
                    result = self.place_limit_order(symbol, side, qty, price)
                    print("Limit Order Result:", result)

                elif choice == '3':
                    symbol = input("Symbol (e.g., BTCUSDT): ")
                    order_id = int(input("Order ID: "))
                    status = self.get_order_status(symbol, order_id)
                    print("Order Status:", status)

                elif choice == '4':
                    print("Exiting.")
                    break

                else:
                    print("Invalid choice. Please select 1–4.")

            except Exception as e:
                logging.error("Unexpected error in CLI loop: %s", str(e))
                print("An error occurred:", str(e))

