FROM python:3.10-alpine

WORKDIR /app/beanie
RUN apk add gcc clang lld musl-dev compiler-rt libffi-dev
RUN pip install poetry
ADD . /app/beanie

RUN poetry install

ENTRYPOINT ["poetry", "run", "beanie"]
