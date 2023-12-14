FROM python:3.11-slim

# install google chrome, chromedriver and add acceptancetest user
RUN apt-get -y update && apt-get install -y curl git wget gnupg jq && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&  \
    LATEST_COMPATIBLE_CHROME_VERSION=$(curl https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | jq -r '.channels."Stable"."version"') && \
    wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${LATEST_COMPATIBLE_CHROME_VERSION}-1_amd64.deb && \
    dpkg -i google-chrome-stable_${LATEST_COMPATIBLE_CHROME_VERSION}-1_amd64.deb || apt -y -f install && \
    rm google-chrome-stable_${LATEST_COMPATIBLE_CHROME_VERSION}-1_amd64.deb && \
    apt-get install -yqq unzip && groupadd --gid 1000 acceptancetests && useradd --create-home --system --uid 1000 --gid acceptancetests acceptancetests

# Chrome and chromedriver share the same version (as of 115) so use this to download chromedriver directly
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Install pipenvm
RUN pip3 install pipenv

# set display port to avoid crash
ENV DISPLAY=:99
WORKDIR /home/acceptancetests

COPY Pipfile* /home/acceptancetests/
RUN pipenv install --system --deploy --dev
USER acceptancetests

RUN mkdir /home/acceptancetests/.postgresql

COPY --chown=acceptancetests . /home/acceptancetests