import os
import time
from loguru import logger
from config import BASEDIR

basedir = BASEDIR

# 定位到log日志文件
log_path = os.path.join(basedir, 'app/logs')

# 创建文件夹
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 日志文件名称
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}.log')

# 具体其他配置 可自行参考 https://github.com/Delgan/loguru
logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True)