import cohere
from dotenv import load_dotenv
import os
load_dotenv()

def getAPI_AI():
    
    return cohere.Client(api_key=os.getenv('KEY_AI'))
