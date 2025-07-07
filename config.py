from os import environ

# Telegram Account Api Id And Api Hash
API_ID = int(environ.get("API_ID", "20284828"))
API_HASH = environ.get("API_HASH", "a980ba25306901d5c9b899414d6a9ab7")

# Your Main Bot Token 
BOT_TOKEN = environ.get("BOT_TOKEN", "7823840798:AAE0WN5tr2tlu1GevJ8TMT10dnHSpiy71rE")

# Owner ID For Broadcasting 
OWNER_ID = int(environ.get("OWNER_ID", "5268762773")) # Owner Id or Admin Id

# Give Your Force Subscribe Channel Id Below And Make Bot Admin With Full Right.
F_SUB = environ.get("F_SUB", "-1002056355467")

# Mongodb Database Uri For User Data Store 
MONGO_DB_URI = environ.get("MONGO_DB_URI", "mongodb+srv://frozenbotss:frozenbots@cluster0.s0tak.mongodb.net/?retryWrites=true&w=majority")

# Port To Run Web Application 
PORT = int(environ.get('PORT', 8080))
