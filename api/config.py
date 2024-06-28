import datetime
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()


EOD_TIMEZONE = datetime.timezone.utc

BASE_DIR = pathlib.Path(__file__).parent
PROJECT_DIR = pathlib.Path(__file__).parent.parent
EOD_API_KEY = os.environ.get('EOD_API_KEY')

