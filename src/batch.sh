INITDATE=20200630
ENDDATE=20200708
CDIR=`pwd`
IMAGE_NAME="yolov4"
CONTAINER_NAME="yolov4_devel"

date=$INITDATE
diff=86410
CAMID=10
while [ ${diff} -ge 86400 ]; do
    echo ${date}
    ndate=`date --date "${date} 1 days" +%Y%m%d`
    # python ./download_fantry.py --sdate ${date}T23:00 --edate ${ndate}T01:00 --camid ${CAMID}
    docker exec -i ${CONTAINER_NAME} /root/miniconda3/bin/python ./count_fantry.py --sdate ${date}T23:00 --edate ${ndate}T01:00 --camid ${CAMID} --output count_${CAMID}.csv
    diff=$((`date --date "${ENDDATE}" +%s` - `date --date "${date}" +%s`))
    date=${ndate}
done

date=$INITDATE
diff=86410
CAMID=11
while [ ${diff} -ge 86400 ]; do
    echo ${date}
    ndate=`date --date "${date} 1 days" +%Y%m%d`
    # python ./download_fantry.py --sdate ${date}T23:00 --edate ${ndate}T01:00 --camid ${CAMID}
    docker exec -i ${CONTAINER_NAME} /root/miniconda3/bin/python ./count_fantry.py --sdate ${date}T23:00 --edate ${ndate}T01:00 --camid ${CAMID} --output count_${CAMID}.csv
    diff=$((`date --date "${ENDDATE}" +%s` - `date --date "${date}" +%s`))
    date=${ndate}
done
