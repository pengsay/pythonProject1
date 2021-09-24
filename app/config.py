from pydantic import BaseSettings
import os

SECRET_KEY = "801790ce713a720cc470ef8a2df914c369bf6f39924fde1734647e8fb1009618"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Setting(BaseSettings):
    f5_username: str = "admin"
    f5_password: str = "1qaz@WSX3edc$RFV"
    f5_root: str = "172.16.66.153"
    db_host: str = "127.0.0.1"
    db_username: str = "root"
    db_pwd: str = "p785084298"
    fw_username: str = "sypeng"
    fw_password: str = "P@ssw0rd"
    fw_root: str = "172.16.66.120"
