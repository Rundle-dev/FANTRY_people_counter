import numpy as np
import os
import glob
import datetime
import subprocess
# import counter


def hourly_downloader(date, camid):
    date = sdate
    hourly_aws_cli(date, date, camid)
    ndate = date + datetime.timedelta(seconds=3600)
    if date.hour == 23:
        # search next day
        hourly_aws_cli(ndate, date, camid)


def hourly_aws_cli(dir_date, file_date, camid, outroot="./"):
    outdir = os.path.join(outroot, dir_date.strftime("%Y-%m-%d"))
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    fname = "{0}??00-{0}??00-{1}.mp4.enc".format(file_date.strftime("%y%m%d%H"),
                                                 camid)
    command = ["aws", "s3", "cp", "--recursive",
                "s3://fantry-videos-prod/{0}/".format(dir_date.strftime("%Y-%m-%d")),
                outdir,
                "--exclude", "*",
                "--include", "{0}".format(fname),
                "--profile", "fantry-prod"]
    subprocess.check_call(command)
    # for 59:00 - 00:00
    ndate = file_date + datetime.timedelta(seconds=3600)
    fname_l = "{0}5900-{1}0000-{2}.mp4.enc".format(file_date.strftime("%y%m%d%H"),
                                                   ndate.strftime("%y%m%d%H"),
                                                   camid)
    command_l = ["aws", "s3", "cp", "--recursive",
                 "s3://fantry-videos-prod/{0}/".format(dir_date.strftime("%Y-%m-%d")),
                 outdir,
                 "--exclude", "*",
                 "--include", "{0}".format(fname_l),
                 "--profile", "fantry-prod"]
    subprocess.check_call(command_l)


def batch_decrypt(date, dataroot="./"):
    datadir = os.path.join(dataroot, date.strftime("%Y-%m-%d"))
    paths = glob.glob(datadir + "/*")
    for path in paths:
        subprocess.check_call(["python", "decrypt/decrypt.py",
                               "-i", path, "-c" "decrypt/decrypt.cfg"])
        subprocess.check_call(["rm", path])


def count_person(date, fps=0.2, dataroot="./"):
    """
    Currently only returns sum_hourly(mean_minute), which is different from
    the actual number of people. But still it is good for estimates in magnitudes.
    """
    datadir = os.path.join(dataroot, date.strftime("%Y-%m-%d"))
    paths = sorted(glob.glob(datadir + "/*"))
    n_persons = []
    for path in paths:
        n_person = np.array(counter.stream_detection(path, fps)).mean()
        n_persons.append(n_person)
    return sum(n_persons)


def main(sdate, edate, camid):
    date = sdate
    while date < edate:
        hourly_downloader(date, camid)
        batch_decrypt(date)
        # n_persons = count_person(date)
        date = date + datetime.timedelta(seconds=3600)

if __name__ == "__main__":
    sdate = datetime.datetime(2020, 5, 20, 23)
    edate = datetime.datetime(2020, 5, 21, 1)
    main(sdate, edate, 10)