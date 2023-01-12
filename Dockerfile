FROM python:3.10.9-bullseye
RUN apt update && apt upgrade -y
RUN pip install flask && pip install -U flask-cors && pip install flask-mysqldb PyMySQL SQLAlchemy pandas flask_login cryptography
ADD "/App" "/root/App"
WORKDIR /root/App
EXPOSE 5000
ENV WAIT_VERSION 2.7.2
ENV WAIT_HOSTS=mysql_db:3306
ENV WAIT_HOSTS_TIMEOUT=300
ENV WAIT_SLEEP_INTERVAL=5
ENV WAIT_HOST_CONNECT_TIMEOUT=30
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait
CMD /wait && /root/App/start.sh