FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libreoffice-writer=1:7.3.4-0ubuntu0.22.04.1 python3-uno=1:7.3.4-0ubuntu0.22.04.1 python3=3.10.4-0ubuntu2 python3-pip=22.0.2+dfsg-1 python3-venv=3.10.4-0ubuntu2 --no-install-recommends -y
RUN apt-get clean
COPY . /app
RUN mkdir ~/.fonts && tar xf /app/fonts.tar.gz --directory ~/.fonts/ && fc-cache -f
WORKDIR /app
CMD ["./start_server"]
