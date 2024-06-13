FROM arm64v8/python:3.12.4-bullseye

RUN mkdir -p /opt/workspace
WORKDIR /opt/workspace
RUN mkdir -p api
COPY requirements.txt api
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r api/requirements.txt

COPY api ./api

WORKDIR /opt/workspace/api
EXPOSE 8010

CMD [ "gunicorn", "--workers=5", "--threads=5", "-b 0.0.0.0:8010", "-k uvicorn.workers.UvicornWorker", "server:app"]
#CMD [ "bash" ]