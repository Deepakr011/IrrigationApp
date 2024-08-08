# app/db/db_config.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

def initialize_db():
    try:
        client = MongoClient(
            "mongodb+srv://deepak:Deepakr123@cluster0.vh0c9g2.mongodb.net/?retryWrites=true&w=majority",
            serverSelectionTimeoutMS=5000  # 5-second timeout
        )
        db = client['IrrigationApp']
        users_collection = db['users']
        # Test connection
        client.admin.command('ping')
        return client, db, users_collection
    except (ConnectionFailure, ConfigurationError) as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        raise
