FROM python:3

WORKDIR /usr/

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./api_poller/api_poller.py" ]