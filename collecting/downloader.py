import requests, os
from tqdm import tqdm

download_path = "http://apk.hiapk.com/appdown/"

def download_file(file):
    with open(file, "rb") as f:
        path = makedir(os.path.abspath(file).replace(".txt", ""))
        for line in f.readlines():
            apk, version, title = line.split(":")
            url = download_path + apk
            title = title.replace("\n","")
            apk_path = makedir(path + "/" + title)

            print url, title, version
            print apk_path

            res = requests.get(url, stream=True, timeout=1000)

            print "[+] size: %dMB" % (float(res.headers['content-length']) / 2**20)

            with open("{}/{}-{}.zip".format(apk_path, title, version), "wb") as f1:
                for chunk in tqdm(res.iter_content()):
                    f1.write(chunk)
e
def makedir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print e

    return path

if __name__ == '__main__':
    download_file("url01.txt")