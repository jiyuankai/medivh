FROM golang:1.12-stretch

WORKDIR /app

COPY ./go.mod /app/go.mod

RUN echo "Asia/Shanghai" > /etc/timezone && \
    sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    apt-get update && \
    apt-get install lsb-release -y && \
    # install mysql-client-5.7
    # https://www.debiantutorials.com/how-to-install-mysql-server-5-6-or-5-7/
#    wget https://dev.mysql.com/get/mysql-apt-config_0.8.9-1_all.deb && \
#    sh -c '/bin/echo -e "4" | dpkg -i mysql-apt-config_0.8.9-1_all.deb' && \
#    apt-get update && \
#    apt-get install mysql-community-client -y --allow-unauthenticated && \
    rm -rf /var/lib/apt

RUN export GOPROXY=https://goproxy.io && go mod download && go get github.com/silenceper/gowatch

