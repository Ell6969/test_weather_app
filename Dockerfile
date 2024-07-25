FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip3 install poetry

RUN poetry config virtualenvs.in-project true

COPY . /code/

RUN poetry install --no-dev

RUN chmod +x /code/entry.sh

EXPOSE 8000

ENTRYPOINT ["/code/entry.sh"]


