from  multi_downloader import *
def single_download():
    single_url = input("请输入视频的播放网址:")
    cookies = get_cookie()
    get_video(single_url,cookies)

def multi_download():
    cid = input("请输入要下载的课程的cid:")
    cookies = get_cookie()
    course_name = get_course_info(cid)
    term = input("请输入学期数:")
    chapters = get_chapters_from_file(course_name+'.json',int(term)-1)
    print("已获取到下列课程信息:")
    # 遍历每个章节
    for chapter in chapters:
        # 获取每个章节的名字
        chapter_name = chapter.get('name').replace('/', '／').replace('\\', '＼')
        print(chapter_name)
        # 获取每个章节对应的所有课程
        courses = get_courses_from_chapter(chapter)
        # 遍历每个章节的所有课程
        for course in courses:
            print("   ",course.get('name'))

    print("开始下载：")
    parents = Path(course_name).absolute()
    parents.mkdir(exist_ok=True)
    flag = 0
    wrong_num = 0
    for chapter in chapters:
        # 获取每个章节的名字
        chapter_name = chapter.get('name').replace('/', '／').replace('\\', '＼')
        # 获取每个章节对应的所有课程
        courses = get_courses_from_chapter(chapter)
        parent = Path(str(parents) + "\\" +str(chapter_name)).absolute()
        parent.mkdir(exist_ok=True)
        # 遍历每个章节的所有课程
        for course in courses:
            # 获取每个课程的播放url
            course_url = get_course_url(course)
            flag += 1
            if flag>=8:
                while True:
                    try:
                        print(f"出错{wrong_num}次")
                        print(f"课程第{flag}个视频开始下载")
                        multi_get_video(course_url,cookies,Path(str(parent)+"\\"+str(course.get('name'))+".mp4"))
                        break
                    except:
                        wrong_num += 1
                        continue



def main():
    while True:
        choice = input("请选择下载方式:\n0.单一视频下载 1.整个课程下载\n")
        if choice == '0':
            single_download()
            break
        elif choice == '1':
            multi_download()
            break
        else:
            print("输入有误，请重新输入")

if __name__ == '__main__':
    main()
