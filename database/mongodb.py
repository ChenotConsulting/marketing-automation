import os
import logging
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

class MongoDB():
    load_dotenv()

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.uri = f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGODB_URL')}/?retryWrites=true&w=majority"
        logging.info(f'MongoDB URL: {self.uri}')

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri)

    def testConnection(self):
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            logging.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logging.error(f'Error pinging MongoDB: {e}')

    def findConfigForUser(self, userId):
        try:
            db = self.client.get_database(name='InsightsAutomation')
            coll = db.get_collection('config')
            config = coll.find_one({"userId": userId})
            logging.info(f'Found config for user {userId}')
            return config
        except Exception as e:
            logging.error(f'Error getting config for user {userId}: \n{e}')
            raise Exception(e)
        