import os
from dotenv import load_dotenv
load_dotenv()
id = os.environ.get('CLIENT_USER')
token = os.environ.get('TOKEN')
print(token)
