import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

class MongoDB():
    load_dotenv()

    def __init__(self):
        self.uri = f"mongodb+srv://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGODB_URL')}/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri)

    def testConnection(self):
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f'Error pinging MongoDB: {e}')

    def findConfigForUser(self, userId):
        try:
            db = self.client.get_database(name='InsightsAutomation')
            coll = db.get_collection('config')
            coll.find_one({"userId": userId})
            print(f'Found config got user {userId}')
            return coll
        except Exception as e:
            print(f'Error getting config for user {userId}: \n{e}')
            raise Exception(e)
        