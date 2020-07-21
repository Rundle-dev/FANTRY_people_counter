CDIR=`pwd`
IMAGE_NAME="test"
CONTAINER_NAME="test_devel"
docker run --name $CONTAINER_NAME --gpus all -v $CDIR/:/share/ -it $IMAGE_NAME /bin/bash
