from flask import g
import logging
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
logging.basicConfig(level=logging.INFO, format="%(message)s")

def log_message(message):
    request_id = g.get('request_id', 'unknown')
    body_message = {'id' : request_id, 'message' : message}
    logging.info(body_message)