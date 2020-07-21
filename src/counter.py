import darknet
import cv2


YOLO_CONFIG_PATH = b"/opt/analysis/darknet/yolov4.cfg"
YOLO_WEIGHTS_PATH = b"/opt/analysis/darknet/yolov4.weights"
YOLO_COCO_DATA_PATH = b"/opt/analysis/FANTRY_people_counter/src/coco.data"

model_yolo_net = darknet.load_net(YOLO_CONFIG_PATH,
                                  YOLO_WEIGHTS_PATH, 0)
model_yolo_meta = darknet.load_meta(YOLO_COCO_DATA_PATH)


def detect_objects(img):
    ret = darknet.detect(model_yolo_net,
                         model_yolo_meta, img)
    return ret


def extract_objects(objects, key=b"person", threshold=0.5):
    detected = [obj for obj in objects
                if obj[0] == key and obj[1] > threshold]
    return detected


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def draw_image(img, objects):
    for obj in objects:
        x, y, w, h = obj[2]
        xmin, ymin, xmax, ymax = convertBack(float(x),
                                             float(y),
                                             float(w),
                                             float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        rect_color = [0, 255, 0]
        cv2.rectangle(img, pt1, pt2, rect_color, 2)
        cv2.putText(img,
                    "{0} [{1:02f}]".format(obj[0].decode(), obj[1]),
                    (pt1[0], pt1[1] + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, rect_color, 4
                    )
    return img


def stream_detection(videopath, fps):
    cap = cv2.VideoCapture(videopath)
    fps_cap = cap.get(cv2.CAP_PROP_FPS)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    spf_desired = 1./fps
    interval = fps_cap * spf_desired
    idx = 0
    num_people = []
    for i in range(num_frames):
        _, frame = cap.read()
        if idx == 0:
            objects = detect_objects(frame)
            objects_extracted = extract_objects(objects)
            num_people.append(len(objects_extracted))
        idx += 1
        if idx >= interval:
            idx = 0
    cap.release()
    return num_people
