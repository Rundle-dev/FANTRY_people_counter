# FANTRY automated people counter from image sequences  

## Functions  
Count people on images via [YOLOv4](https://github.com/AlexeyAB/darknet).  
To reduce computational complexity, images are only evaluated in every 5 seconds.  
  
## Preparation  
Place decryption cofiguration (decrypt.cfg) file at src/decrypt/.  
Edit contents if applicable.  
  
## Usage  
Download encrypted videos and decode them.  
```bash
python download_fantry.py --sdate ${YYYYMMDDTHH:MM} --edate ${YYYYMMDDTHH:MM} --camid ${CAMERA_ID}
```
  
Count people on images.  
```bash
python count_fantry.py --sdate ${YYYYMMDDTHH:MM} --edate ${YYYYMMDDTHH:MM} --camid ${CAMERA_ID} --output ${OUTPUT_CSV}
```
  
To change an evaluation interval in seconds, add `--fps ${value}` argument.  
If not specified, fps=0.2 (image/5-seconds) is used.  
  
Or just use a batch script to do them both:  
```bash
sh batch.sh
```
  
## Notes  
- work with minimal via the instance type x3s.large  
- aws cli command is used in the scripts. A configuration (--profile fantry-prod) is needed.  
- Usual runtime for an 1-hr video is 7-8min.  
- Data size is 600MB/hr.  
