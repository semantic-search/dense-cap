FROM nagadomi/torch7:latest
#Densecap Dependencies
RUN luarocks install nn
RUN luarocks install image
RUN luarocks install lua-cjson
RUN luarocks install https://raw.githubusercontent.com/jcjohnson/torch-rnn/master/torch-rnn-scm-1.rockspec
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install wget
# rebuilding cmake
RUN apt-get purge -y cmake
RUN git clone https://github.com/Kitware/CMake.git
RUN apt-get install libssl-dev
RUN cd CMake && ./bootstrap; make; sudo make install
#download densecap
RUN git clone https://github.com/jcjohnson/densecap.git
WORKDIR densecap
COPY . .
RUN pip3 install -r requirements.txt
RUN sh scripts/download_pretrained_model.sh