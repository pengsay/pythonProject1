from pydantic import BaseSettings
import os

SECRET_KEY = "801790ce713a720cc470ef8a2df914c369bf6f39924fde1734647e8fb1009618"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Setting(BaseSettings):
    f5_username: str = "admin"
    f5_password: str = "admin"
    f5_root: str = "172.16.60.68"
    db_host: str = "app-db"
    db_username: str = "foresight"
    db_pwd: str = "foresight"
    fw_username: str = "admin"
    fw_password: str = "1qaz@WSX3edc"
    fw_root: str = "172.16.66.120"
