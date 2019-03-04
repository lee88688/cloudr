import os
import shutil
from hashlib import md5
from model.db_model import Session, OfflineDownload, File, FileType
from .celery import app
from utils.aria2 import Aria2
from config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN, FILE_PATH


aria2 = Aria2(ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN)
