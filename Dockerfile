FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./weather_app/ /code/

COPY ./entry.sh /code/

EXPOSE 8000

ENTRYPOINT ["sh", "/code/entry.sh"]
