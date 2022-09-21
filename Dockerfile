FROM python:3.10

RUN apt-get update && \
    apt-get install -y && \
    python -m pip install --upgrade pip

COPY . /home
WORKDIR /home

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

RUN chmod +x /home/start.sh
ENTRYPOINT /home/start.sh
