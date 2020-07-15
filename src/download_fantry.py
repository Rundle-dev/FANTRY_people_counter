import numpy as np
import os
import glob
import argparse
import datetime
import subprocess


def hourly_downloader(date, camid):
    hourly_aws_cli(date, date, camid)
    ndate = date + datetime.timedelta(seconds=3600)
    if date.hour == 23:
        # search next day
        hourly_aws_cli(ndate, date, camid)


def hourly_aws_cli(dir_date, file_date, camid, outroot="./"):
    outdir = os.path.join(outroot, file_date.strftime("%Y-%m-%d"), "{0:02d}".format(file_date.hour))
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
    datadir = os.path.join(dataroot, date.strftime("%Y-%m-%d"), "{0:02d}".format(date.hour))
    paths = glob.glob(datadir + "/*.enc")
    for path in paths:
        print(path)
        subprocess.check_call(["python", "decrypt/decrypt.py",
                               "-i", path, "-c" "decrypt/decrypt.cfg"])
        subprocess.check_call(["rm", path])


def main(sdate, edate, camid):
    date = sdate
    while date < edate:
        hourly_downloader(date, camid)
        batch_decrypt(date)
        date = date + datetime.timedelta(seconds=3600)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download video from S3 [hourly]")
    parser.add_argument("--sdate", help="start date [%Y%m%dT%H:%M]", type=str, required=True)
    parser.add_argument("--edate", help="end date [%Y%m%dT%H:%M]", type=str, required=True)
    parser.add_argument("--camid", help="camera id", type=int, required=True)
    args = parser.parse_args()
    sdate = datetime.datetime.strptime(args.sdate, "%Y%m%dT%H:%M")
    edate = datetime.datetime.strptime(args.edate, "%Y%m%dT%H:%M")
    main(sdate, edate, args.camid)
