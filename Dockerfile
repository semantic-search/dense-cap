FROM nagadomi/torch7:latest
# Densecap Dependencies
RUN luarocks install nn
RUN luarocks install image
RUN luarocks install lua-cjson
RUN luarocks install https://raw.githubusercontent.com/jcjohnson/torch-rnn/master/torch-rnn-scm-1.rockspec

# Densecap
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install wget
RUN cd /root/ && git clone https://github.com/jcjohnson/densecap && cd /root/densecap/
RUN /root/densecap/scripts/download_pretrained_model.sh
RUN apt-get purge -y cmake
RUN git clone https://github.com/Kitware/CMake.git
RUN apt-get install libssl-dev
RUN cd CMake && ./bootstrap; make; sudo make install

# Set ~/torch as working directory
WORKDIR /root/densecap
RUN sh scripts/download_pretrained_model.sh
RUN apt-get install -y python3-pip
RUN pip3 install redis python-dotenv kafka-python
COPY main.py . 
CMD ["python", "main.py"]
