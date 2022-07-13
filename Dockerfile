FROM joyzoursky/python-chromedriver:3.9

RUN pip3 install pipenv
RUN apt-get update -y && apt-get install -y curl git && groupadd --gid 1000 acceptancetests && \
    useradd --create-home --system --uid 1000 --gid acceptancetests acceptancetests

#Setup for Chrome/ChromeDriver for web UI testing
RUN apt install -y wget unzip
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata


WORKDIR /home/acceptancetests

COPY Pipfile* /home/acceptancetests/
RUN pipenv install --system --deploy --dev
USER acceptancetests

RUN mkdir /home/acceptancetests/.postgresql

COPY --chown=acceptancetests . /home/acceptancetests
