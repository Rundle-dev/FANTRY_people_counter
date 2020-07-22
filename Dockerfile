FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu16.04

RUN apt update && apt install -y git wget unzip
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN sh Miniconda3-latest-Linux-x86_64.sh -b
RUN /root/miniconda3/bin/conda init
RUN /root/miniconda3/bin/conda install -y opencv pandas

RUN mkdir -p /opt/analysis/
WORKDIR /opt/analysis/
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR /opt/analysis/darknet
RUN sed -i "s|GPU=0|GPU=1|g" Makefile
RUN sed -i "s|CUDNN=0|CUDNN=1|g" Makefile
RUN sed -i "s|LIBSO=0|LIBSO=1|g" Makefile
RUN make
RUN wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
RUN sed -i "s|batch=64|batch=1|g" yolov4.cfg
RUN sed -i "s|subdivisions=8|subdivisions=1|g" yolov4.cfg
RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

WORKDIR /opt/analysis/
RUN wget http://zebulon.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-637.x86_64-unknown-linux.zip
RUN unzip Bento4-SDK-1-6-0-637.x86_64-unknown-linux.zip
RUN mv Bento4-SDK-1-6-0-637.x86_64-unknown-linux Bento4

WORKDIR /opt/analysis/
RUN wget https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
RUN unzip awscli-exe-linux-x86_64.zip
RUN ./aws/install

WORKDIR /opt/analysis/
RUN git clone https://github.com/windsor718/FANTRY_people_counter.git

WORKDIR /opt/analysis/FANTRY_people_counter/src/