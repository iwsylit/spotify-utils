FROM python:3.9-alpine

COPY . /app
WORKDIR app

RUN apk update

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

EXPOSE 9876:9876

WORKDIR api
CMD ["sh", "run.sh"]
