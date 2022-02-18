import requests
import re
import json
from pathlib import Path
from Crypto.Cipher import AES
import os
#格式化cookie为字典，以便requests使用
def format_cookie():
    cookies = {}
    for i in json.loads(Path('cookies.json').read_bytes()):
        cookies.update({i['name']: i['value']})
    return cookies

# 从key文件中读取key
def get_key(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

# 内容解密
def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

# 文件解密
def decrypt_file(filename, key):
    with open("./downloads/" + filename, 'rb') as f:
        ciphertext = f.read()
    dec = decrypt(ciphertext, key)
    with open("./decrypt/" + filename, 'wb') as f:
        f.write(dec)

# ts文件合并转换为mp4文件
def ts2mp4(n,video):
    file_name = "0.ts"
    for i in range(1, n):
        file_name = file_name + f"+{i}.ts"
    os.system("cd decrypt&&copy /b " + file_name + " " + str(video))
    os.system("cd downloads&&del *.ts")
    os.system("cd decrypt&&del *.ts")
    os.system("del get_dk")
    print(str(video.stem)+" 合并转换完成")

# 进度条
def progress_bar(words,now,total):
    print("\r"+words+":   "+"▋"*(now*50//total),str((now*100/total))+"%",end="")

def download(m3u8_url,video):
    # 从m3u8链接中取出需要的前缀和后缀
    pattern2 = re.compile(r'(?P<prefix>.*?)voddrm.token.*?exper=0(?P<suffix>.*)', re.S)
    res = pattern2.finditer(m3u8_url)
    for i in res:
        prefix = i.group("prefix")
        suffix = i.group("suffix")

    # 获取m3u8文件
    m3u8_resp = requests.get(m3u8_url, cookies=format_cookie())
    with open("m3u8", "wb") as f:
        f.write(m3u8_resp.content)

    #拿视频解密要用的key
    pattern1 = re.compile(r'URI="(?P<key>.*?)"')
    res = pattern1.finditer(m3u8_resp.text)
    for i in res:
        key_url = i.group("key")
    key_resp = requests.get(key_url)
    with open("get_dk", "wb") as f:
        f.write(key_resp.content)
    key = get_key("get_dk")
    print("成功拿到key")

    # 计算总数
    num = 0
    with open("m3u8", "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            num+=1

    # 读取m3u8文件开始下载
    n = 0
    with open("m3u8", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            single_ts_url = prefix + line + suffix
            # print(single_ts_url)
            single_ts_resp = requests.get(single_ts_url, cookies=format_cookie())
            download_file = Path("downloads").absolute()
            download_file.mkdir(exist_ok=True)
            with open(str(download_file) +"/"+ f"{n}.ts", "wb") as f:
                f.write(single_ts_resp.content)
            progress_bar(str(video.stem)+" 的下载进度",n+1,num)
            n = n + 1
        print(str(video.stem)+" 下载完成")

    # 按照下载的文件名依次解密
    decrypt = Path("decrypt").absolute()
    decrypt.mkdir(exist_ok=True)
    for i in range(n):
        filename = f"{i}.ts"
        decrypt_file(filename, key)
        progress_bar(str(video.stem)+" 的解密进度",i+1,num)
    print(str(video.stem)+" 解密完成")
    ts2mp4(n,video)




