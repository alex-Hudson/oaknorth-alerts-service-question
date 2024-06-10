FROM python:3.11 AS build

COPY poetry.lock pyproject.toml /code/

WORKDIR /code/

RUN pip install --upgrade pip poetry==1.7.0 \
    && poetry self add poetry-plugin-export==1.6.0 \
    && poetry export > requirements.txt

FROM python:3.11 as runtime

COPY --from=build /code/requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR "/code/"

CMD uvicorn --host 0.0.0.0 --reload --reload-dir=/code/alerts_service/ alerts_service.app:app
