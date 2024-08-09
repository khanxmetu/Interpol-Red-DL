FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD streamlit run notice_dashboard/Notice_Dashboard.py --server.port 5000