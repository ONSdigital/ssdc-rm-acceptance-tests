FROM python:3.11-slim

# install google chrome, chromedriver and add acceptancetest user
RUN apt-get -y update && apt-get install -y curl git wget gnupg && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&  \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
&& apt-get -y update || true && apt-get install -y google-chrome-stable && apt-get install -yqq unzip && groupadd --gid 1000 acceptancetests && useradd --create-home --system --uid 1000 --gid acceptancetests acceptancetests

# Chrome and chromedriver share the same version (as of 115) so use this to download chromedriver directly
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Install pipenv
RUN pip3 install pipenv

# set display port to avoid crash
ENV DISPLAY=:99
WORKDIR /home/acceptancetests

COPY Pipfile* /home/acceptancetests/
RUN pipenv install --system --deploy --dev
USER acceptancetests

RUN mkdir /home/acceptancetests/.postgresql

COPY --chown=acceptancetests . /home/acceptancetests