import numpy as np
import pandas as pd
import os
import glob
import argparse
import datetime
import subprocess
import counter


def count_person(date, fps=0.2, dataroot="./", coef=60):
    """
    Currently only returns sum_hourly(mean_minute*60), which is different from
    the actual number of people. But still it is good for estimates in magnitudes.
    """
    datadir = os.path.join(dataroot, date.strftime("%Y-%m-%d"))
    paths = sorted(glob.glob(datadir + "/*"))
    n_persons = []
    for path in paths:
        n_person = np.array(counter.stream_detection(path, fps)).mean()*coef
        n_persons.append(n_person)
    return sum(n_persons)


def main(sdate, edate, camid, fps, outpath):
    date = sdate
    dates = []
    nums = []
    while date < edate:
        n_persons = count_person(date, fps=fps)
        dates.append(date)
        nums.append(n_persons)
        date = date + datetime.timedelta(seconds=3600)
    df = pd.DataFrame([dates, nums], columns=["Date", "count"])
    if os.path.exists(outpath):
        df.to_csv(outpath, index=False)
    else:
        df.to_csv(outpath, index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="count a sum of person per frame in videos via YOLOv4")
    parser.add_argument("--sdate", help="start date [%Y%m%dT%H:%M]", type=str, required=True)
    parser.add_argument("--edate", help="end date [%Y%m%dT%H:%M]", type=str, required=True)
    parser.add_argument("--camid", help="camera id", type=int, required=True)
    parser.add_argument("--fps", help="fps", type=float, default=0.2, required=False)
    parser.add_argument("-o", "--output", help="output csv file path",
                        type=str, default="./count.csv", required=False)
    args = parser.parse_args()
    sdate = datetime.datetime.strptime(args.sdate, "%Y%m%dT%H:%M")
    edate = datetime.datetime.strptime(args.edate, "%Y%m%dT%H:%M")
    main(sdate, edate, args.camid, args.fps, args.output)
