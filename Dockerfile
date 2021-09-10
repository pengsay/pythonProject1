FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

RUN pip install -r /app/requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/