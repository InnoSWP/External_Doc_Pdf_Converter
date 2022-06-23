FROM ubuntu:latest
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libreoffice python3 python3-pip python3-venv -y
COPY . /app
WORKDIR /app
CMD ["./start_server"]
