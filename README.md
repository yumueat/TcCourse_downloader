# 腾讯课堂视频下载器

## 简介 

本程序可以用于下载腾讯课堂对应账号可以播放的视频（也就是说并不是白嫖），提供单个视频下载和整个课程下载两种下载方式。

## 用法

### 单个视频下载

先选择下载方式

![image](https://user-images.githubusercontent.com/87589322/154710343-803e2a84-1703-4b12-a4b8-0d26452567d4.png)

然后输入播放页面的网址

![image](https://user-images.githubusercontent.com/87589322/154710393-2dd7090e-10a8-4072-b70d-cefb47b06a07.png)

就是这个

![image](https://user-images.githubusercontent.com/87589322/154711505-06336fd1-7708-41f6-a778-5bc6b14b4a7e.png)

然后会弹出登录窗口，登录后会记录下cookie信息，以便后面的下载（值得一提的是cookie有时间限制，一般每一天都得换，只要删除掉cookies.json文件程序就会重新打开登录页面记录cookie），然后就可以选择码率

![image](https://user-images.githubusercontent.com/87589322/154711687-aeaf609e-da78-4c6b-a88b-e408acc86d4a.png)

然后就开始下载了

![image](https://user-images.githubusercontent.com/87589322/154711640-19e3e032-274b-4851-a952-897051358471.png)

下载完成后会开始解密

![image](https://user-images.githubusercontent.com/87589322/154711758-9de5c32b-b3f7-4c5d-b45e-b50fb8a98c1c.png)

之后会提示视频合并转换完成，到此视频就下载完成了，可以在python文件对应的文件夹下面找到

![image](https://user-images.githubusercontent.com/87589322/154711768-804c7235-8ebb-4ed5-9e20-fb6a3d838c14.png)

### 整个课程下载

如图

![image](https://user-images.githubusercontent.com/87589322/154711798-900eb872-0a0e-4c51-949a-a1c4e85b4f20.png)

cid在url里面找，如图

![image](https://user-images.githubusercontent.com/87589322/154711818-a523eeb4-042a-471a-9b80-537c93d02bbc.png)

班级在课程任务页能找到，如图

![image](https://user-images.githubusercontent.com/87589322/154711850-e18f85f8-c400-47c5-baf9-78f6e17a47d6.png)

其他没什么要解释的了，按照要求输入就行了，提示也写的很清楚了，然后就会输出获取到的课程信息，接着就开始下载了，后面的和之前的单个视频下载都差不多，就不一一截屏了，最后视频会存放在以课程名字为主文件夹，章节名字为子文件的目录下（与python文件在同一个目录下）

![image](https://user-images.githubusercontent.com/87589322/154711884-611a578d-5b50-4543-836b-4297ab10ab13.png)

### 高级用法（选择整个课程中需要下载的视频）

修改`downloader.py`文件中第42行（行数可能变化，以实际的为准）的判断语句，如图

![image](https://user-images.githubusercontent.com/87589322/154711935-6121e4cb-d2c1-4735-895a-329e373bde93.png)

flag表示的是下载的视频的序号，这里的`flag>=16`就是从第16个视频开始下载的意思，再比如要下载第13、16、18个视频，就把判断条件改为`flag == 13 or flag ==16 or flag ==18`即可

## 一些可能遇到的情况（注意事项）

+ 本程序仅适用于Windows系统

+ 要输入的学期指的是在课程主页看到的班级情况，比如

![image](https://user-images.githubusercontent.com/87589322/154711949-0c19bf11-ab39-4349-8466-58cfe37059cb.png)

  这个时候就输入数字1就好了，但有些时候班级并不是这样显示的，比如

![image](https://user-images.githubusercontent.com/87589322/154711986-35ad5a85-6756-428d-806f-4319c1a525f1.png)

  ~~这时候需要去`https://ke.qq.com/cgi-bin/course/basic_info?cid=`查看自己对应的学期信息（cid=后面要跟课程cid），有些时候会报错，这是可以考虑通过下面的代码来获取课程信息（返回的是json格式的，对着看就行了）~~

  ```python
  import requests
  headers = { "referer":"https://ke.qq.com/letter/index.html"}
  url = "https://ke.qq.com/cgi-bin/course/basic_info?cid=2739211" #这里的url只是例子
  resp = requests.get(url,headers=headers).json()
  print(resp.get('result').get('course_detail').get('terms'))
  ```

  **但是**上面的方法挺麻烦的，所以我的建议是直接从1开始试，一方面很多的课程都只有一个学期，一般输1就可以了，如果1不行慢慢往后试就好

+ 一些报错，诸如下面这类并不影响程序的运行，所以当发现报错时先看看视频有没有下载成功（在文件夹里面查看），如果成功了就不用管了（PS：重启程序解决90%的问题）

![image](https://user-images.githubusercontent.com/87589322/154712066-80dabf6b-e39c-437f-a936-cd5981b0f502.png)

![image](https://user-images.githubusercontent.com/87589322/154712080-6078ea9a-ba15-4133-a800-2fb9376c5376.png)

+ 下面这种情况代表程序在运行过程中出现了错误然后自动重新运行，如果自动重新运行后程序表面上长期没有进展，那就手动重启吧

![image](https://user-images.githubusercontent.com/87589322/154712137-dfcca76a-8b48-4e5c-89e8-853a0d82d940.png)

+ 如果进度条长时间没动，可以考虑手动重启程序，如果是在整个课程下载的时候出现这种情况，可以考虑跳过当前的视频，先下载其他的视频，因为有些视频比较难下载，这样会把整个进程卡住

+ 如果发现了程序的什么问题，欢迎提交

## TODO

+ ~~增加标识符，以便控制课程中具体要下载的视频~~
+ ~~增加自动重试功能，对抗因网络原因导致的失败问题~~
+ ~~增加错误次数显示，以便灵活选择是否继续下载~~

+ 把下载改为多线程+异步协程的方式，加快下载速度
+ 修改代码以便在Linux系统上运行
