import pymongo
import os
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")
CLIENT = pymongo.MongoClient(os.getenv("MONGO_URL"))
DATABASE = CLIENT.EscapeRoom.production
