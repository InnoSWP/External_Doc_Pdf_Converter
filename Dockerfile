FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libreoffice-writer python3-uno python3 python3-pip python3-venv --no-install-recommends -y
RUN apt-get clean
COPY . /app
WORKDIR /app
CMD ["./start_server"]
