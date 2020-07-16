# FANTRY automated people counter from image sequences  

## Functions  
Count people on images via [YOLOv4](https://github.com/AlexeyAB/darknet).  
To reduce computational complexity, images are only evaluated in every 5 seconds.  
  
## Preparation  
instance type: g3xs.large (GPU instance)
Place decryption cofiguration (decrypt.cfg) file at src/decrypt/.  
Edit contents if applicable.  
  
## Usage  
Download encrypted videos and decode them.  
```bash
python download_fantry.py --sdate ${YYYYMMDDTHH:MM} --edate ${YYYYMMDDTHH:MM} --camid ${CAMERA_ID}
```
  
count people on images.  
```bash
python count_fantry.py --sdate ${YYYYMMDDTHH:MM} --edate ${YYYYMMDDTHH:MM} --camid ${CAMERA_ID} --output ${OUTPUT_CSV}
```
  
To change an evaluation interval in seconds, add `--fps ${value}` argument.  
If not specified, fps=0.2 (image/5-seconds) is used.  
  
## ToDo  
- add Bento-4 download/compilation in Dockerfile.  
