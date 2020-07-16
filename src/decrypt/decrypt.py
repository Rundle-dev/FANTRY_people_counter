import os
import subprocess
import configparser
import argparse

parser = argparse.ArgumentParser(description="decrypt mp4")
parser.add_argument("-c", "--config", type=str, required=True)
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-o", "--output", type=str, required=False,
                    default="remainsame")
args = parser.parse_args()
if args.output == "remainsame":
    filename = args.input.split("/")[-1].split(".")[0]
    args.output = os.path.join(os.path.dirname(args.input),
                               "{0}.mp4".format(filename))
    print(args.output)
config = configparser.ConfigParser()
config.read(args.config)
decrypt_key = config.get("decryption", "decrypt_key")
path_to_Bento = config.get("decryption", "path_to_Bento")
inppath = args.input
outpath = args.output
subprocess.check_call([os.path.join("{0}".format(path_to_Bento),
                                    "mp4decrypt"),
                       "--key",
                       "1:{0}:random".format(decrypt_key),
                       "--key",
                       "2:{0}:random".format(decrypt_key),
                       inppath, outpath])
