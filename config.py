import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    UPLOADED_PHOTOS_DEST = 'page_data/screenshots'
