from basic_bot import BasicBot

API_KEY = "your_testnet_api_key"
API_SECRET = "your_testnet_api_secret"

bot = BasicBot(API_KEY, API_SECRET)
bot.run_cli()