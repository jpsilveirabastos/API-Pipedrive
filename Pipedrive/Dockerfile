FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /pipedrive

COPY ./requirements.txt /pipedrive/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /pipedrive/requirements.txt

COPY ./app /pipedrive/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
