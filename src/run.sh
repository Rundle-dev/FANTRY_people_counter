CDIR=`pwd`
IMAGE_NAME="yolov4"
CONTAINER_NAME="yolov4_devel"
docker run --name $CONTAINER_NAME --gpus all -v $CDIR/:/share/ -it $IMAGE_NAME /bin/bash
