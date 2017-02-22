FROM ubuntu:16.04
RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV USER root
WORKDIR /root
RUN apt-get update -y -o DPkg::Options::=--force-confold && apt-get upgrade -y -o DPkg::Options::=--force-confold
RUN apt-get install -y -o DPkg::Options::=--force-confold wget unzip xdotool git python2.7 python2.7-dev python-pip gettext build-essential
RUN easy_install -U pip

ADD requirements.txt ./
RUN pip install -r requirements.txt

#vncserver
RUN apt-get install -y -o DPkg::Options::=--force-confold tightvncserver fluxbox xterm
RUN mkdir .vnc && chmod 700 .vnc && echo 'test37' | vncpasswd -f > .vnc/passwd && chmod 600 .vnc/passwd
RUN echo "#!/bin/bash" >> .vnc/xstartup && echo "exec /usr/bin/fluxbox" >> .vnc/xstartup && chmod 755 .vnc/xstartup
ENV DISPLAY :35
EXPOSE 5935

#chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && apt-get update -y -o DPkg::Options::=--force-confold && apt-get install -y -o DPkg::Options::=--force-confold google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && chmod +x chromedriver && mv chromedriver /usr/local/bin/ && rm chromedriver_linux64.zip
# https://bugs.chromium.org/p/chromium/issues/detail?id=519952#c8
#volumes: /dev/shm:/dev/shm

WORKDIR /clicker

#docker build -t clicker .
#docker run -it --rm -p 5935:5935 -v `pwd`:/clicker clicker bash
#vncserver :35 -geometry 1400x1050
#python main.py https://www.youtube.com/watch?v=l8F2g7I-qh0 pattern.png

