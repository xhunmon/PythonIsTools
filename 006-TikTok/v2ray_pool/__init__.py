# 运行时路径。并非__init__.py的路径
import os
import sys

BASE_DIR = "../002-V2rayPool"
if os.path.exists(BASE_DIR):
    sys.path.append(BASE_DIR)

from core import utils
from core.conf import Config
from db.db_main import DBManage