# Clicker

## Description

Python script to handle URLs, get position of the image on the screen and
click on the found position.

## Technologies

- Language: Python 2.7

- Libraries: OpenCV, Selenium

## Prerequisites

`xdotool`, `opencv` packages and selenium driver installed
[selenium installation](https://github.com/SeleniumHQ/selenium/blob/master/py/docs/source/index.rst).

## Usage

The script has two required arguments: URL and path to the image.

```
git clone https://yevheniia1393@bitbucket.org/yevheniia1393/quantu.git
cd quantu/
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py https://www.youtube.com/watch?v=l8F2g7I-qh0 pattern.png
```

## Usage via docker

Build image once

```
docker build -t clicker .
```

Run


```
docker run -it --rm -p 5935:5935 -v `pwd`:/clicker clicker bash
vncserver :35 -geometry 1400x1050
python main.py https://www.youtube.com/watch?v=l8F2g7I-qh0 pattern.png
```

On machine with X11 start vncviewer and connect to IP of host running clicker and port 5935, for instance

```
vncviewer 127.0.0.1:5935
```
