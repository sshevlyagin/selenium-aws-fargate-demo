FROM python:3.6

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update --fix-missing
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install browsermob proxy, needed for selenium_browsermob
RUN wget -O /tmp/browsermob-proxy.zip https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
RUN unzip /tmp/browsermob-proxy.zip -d /usr/local/bin/

# install java, needed for selenium_browsermob
RUN apt-get install -y openjdk-8-jre

# set display port to avoid crash
ENV DISPLAY=:99

# Install requirements first so this step is cached by Docker
COPY /requierments.txt /home/selenium-aws-fargate-demo/requirements.txt
WORKDIR /home/selenium-aws-fargate-demo/
RUN pip install -r requirements.txt

# copy code
COPY ./ /home/selenium-aws-fargate-demo/
RUN python setup.py install