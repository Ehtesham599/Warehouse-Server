FROM python:3.8-slim

ENV PORT 8080
ENV APPDIR /app
ENV APPNAME warehouse-server

WORKDIR $APPDIR

COPY . $APPDIR

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]