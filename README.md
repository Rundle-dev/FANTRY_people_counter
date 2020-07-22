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
  
Or just use batch script to do them both:  
```bash
sh batch.sh
```
  
## Notes  
- aws cli command is used in the scripts. A configuration (--profile fantry-prod) is needed.  
- Usual runtime for an 1-hr video is 8min.  
- Data size is 600MB/hr.  
