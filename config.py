from os import environ

# Telegram Account Api Id And Api Hash
API_ID = int(environ.get("API_ID", "20284828"))
API_HASH = environ.get("API_HASH", "a980ba25306901d5c9b899414d6a9ab7")

# Your Main Bot Token 
BOT_TOKEN = environ.get("BOT_TOKEN", "7649485504:AAH3LSTdAOlZc1kjN3ZzpqDZBvvlPFLWA5E")

# Owner ID For Broadcasting 
OWNER_ID = int(environ.get("OWNER_ID", "6797820880")) # Owner Id or Admin Id

# Give Your Force Subscribe Channel Id Below And Make Bot Admin With Full Right.
F_SUB = environ.get("F_SUB", "-1002393689329")

# Mongodb Database Uri For User Data Store 
MONGO_DB_URI = environ.get("MONGO_DB_URI", "mongodb+srv://yacan69355:Cw92BrnfAfWQcLvU@cluster0.jh6h6wg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Port To Run Web Application 
PORT = int(environ.get('PORT', 8080))
