FROM ghcr.io/semantic-search/densecap_gpu:latest
RUN luarocks install https://raw.githubusercontent.com/jainal09/stnbhwd/master/stnbhwd-scm-1.rockspec
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 main.py