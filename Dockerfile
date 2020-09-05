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
# recursively clonning
RUN git clone --recurse-submodules https://github.com/semantic-search/dense-cap.git
WORKDIR dense-cap
RUN sh densecap/scripts/download_pretrained_model.sh
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]