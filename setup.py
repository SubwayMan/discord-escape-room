from getpass import getpass

bot_token = getpass("Discord bot token: ")
mongo_token = getpass("MongoDB Atlas API token: ")

with open(".env", "w") as f:
    f.write(f"TOKEN=\"{bot_token}\"\nMONGO_URL=\"{mongo_token}\"")

print(".env file created.")
