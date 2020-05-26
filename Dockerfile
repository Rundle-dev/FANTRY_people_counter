FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu16.04

RUN apt update && apt install -y git wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN sh Miniconda3-latest-Linux-x86_64.sh -b
RUN /root/miniconda3/bin/conda init
RUN /root/miniconda3/bin/conda install -y opencv

RUN mkdir -p /opt/analysis/
WORKDIR /opt/analysis/
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR /opt/analysois/darknet
RUN sed -i "s|GPU=0|GPU=1|g" Makefile_copy
RUN sed -i "s|CUDNN=0|CUDNN=1|g" Makefile_copy
RUN sed -i "s|LIBSO=0|LIBSO=1|g" Makefile_copy
RUN make
RUN wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
