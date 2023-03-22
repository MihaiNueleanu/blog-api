FROM python:3.8

RUN apt-get install curl
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

RUN $HOME/.poetry/bin/poetry install

CMD $HOME/.poetry/bin/poetry run uvicorn main:app --host 0.0.0.0