from classes import MyBot
import os
from dotenv import load_dotenv

load_dotenv(".env")

bot = MyBot()
bot.run(os.getenv("TOKEN"))
