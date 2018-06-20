FROM python:3
LABEL name "simple-keras-rest-api"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 6543
CMD ["python", "./server.py"]