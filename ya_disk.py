import os
import yadisk

from dotenv import load_dotenv
load_dotenv()

YA_TOKEN = os.getenv('YA_TOKEN')
YA_REMOTE_PATH = os.getenv('YA_REMOTE_PATH')
YA_LOCAL_PATH = os.getenv('YA_LOCAL_PATH')

y = yadisk.YaDisk(token=YA_TOKEN)
