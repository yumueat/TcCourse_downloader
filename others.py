from playwright.sync_api import Playwright, sync_playwright
from utils import *

# 模拟登录获取cooikie
def run_browser2get_cookie(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ke.qq.com/")
    page.click("#js-mod-entry-index >> text=登录")
    page.wait_for_selector('.login-mask', state='attached')
    page.wait_for_selector('.login-mask', state='detached')
    cookie = page.context.cookies()
    page.close()
    context.close()
    browser.close()
    with open("cookies.json","w") as f:
        f.write(json.dumps(cookie))

# 通过播放页的url获取对应的m3u8链接
def run_browser2get_m3u8_info(playwright : Playwright, play_url : str, playlist_url : list,course_name : list,flag : bool,cookies) -> None:
    browser = playwright.chromium.launch(headless=True,devtools=True)
    context = browser.new_context()
    page = context.new_page()
    page.context.add_cookies(cookies)
    def filter(response):
        if ".m3u8" in response.url:
            playlist_url.append(response.url)
    page.on("response",filter)
    page.goto(play_url)
    while len(playlist_url) < 2 :
        playlist_url.clear()
        page.on("response", filter)
        page.goto(play_url)
    if flag:
        course_name.append(str(page.query_selector("#react-body >> div.study-header >> div.current-task-name.header-item").text_content()))
    resp = requests.get(playlist_url[0],cookies=format_cookie())
    with open("playlist.txt","wb") as f:
        f.write(resp.content)

#获取cookie，返回json格式的cookie
def get_cookie():
    cookies_file = Path("cookies.json")
    if cookies_file.exists():
        print("检测到cookie")
    else:
        with sync_playwright() as playwright:
            run_browser2get_cookie(playwright)
        if cookies_file.exists():
            print("已获取cookie")
        else:
            print("程序出错，请重试或者手动添加cookie")
            exit(0)
    cookies = json.loads(cookies_file.read_bytes())
    return cookies

# 通过播放页面url下载视频
def get_video(play_url : str , cookies ):
    playlist_url = []
    course_name = []
    with sync_playwright() as playwright:
        run_browser2get_m3u8_info(playwright,play_url,playlist_url,course_name,True,cookies)
    playlist = Path("playlist.txt")
    resolution_list = []
    m3u8_list = []
    flag = 0
    with open(playlist,"r") as f:
        for i in f:
            i.strip()
            if i.startswith("#EXT-X-STREAM-INF"):
                resolution_list.append(i)
                flag =1
                continue
            if flag == 1:
                flag = 0
                m3u8_list.append(i)
    print("检测到有以下码率可供选择，请选择要下载的资源(网络原因可能导致某些码率下载不了，此时会选择尽可能高的码率下载)\n")
    n=0
    for i in resolution_list:
        print(f"{n}.",resolution_list[n],end="")
        n+=1
    choice = input()
    video = Path(course_name[0] + ".mp4").absolute()
    try:
        download(playlist_url[choice+1],video)
    except:
        download(playlist_url[-1],video)

def multi_get_video(play_url : str , cookies,video):
    playlist_url = []
    course_name = []
    with sync_playwright() as playwright:
        run_browser2get_m3u8_info(playwright, play_url, playlist_url, course_name,False, cookies)
    download(playlist_url[-1], video)