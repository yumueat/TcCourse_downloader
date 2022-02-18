from others import *
# 获取课程信息，存在以课程名称为文件名的json文件中，并返回课程名字
def get_course_info(cid):
    url = 'https://ke.qq.com/cgi-bin/course/basic_info?cid=' + str(cid)
    headers = { "referer":"https://ke.qq.com/letter/index.html"}
    response = requests.get(url,headers=headers).json()
    while response == {'msg': 'refer错误', 'type': 1, 'retcode': 100101}:
        response = requests.get(url).json()
    # print(response)
    # exit(0)
    course_name = response.get('result').get('course_detail').get('name').replace('/', '／').replace('\\', '＼')
    with open(course_name + '.json', 'w') as f:
        f.write(json.dumps(response))
    return  course_name

# 从存放课程信息的文件中获取章节信息
def get_chapters_from_file(filename, term_index):
    with open(filename, 'r') as f:
        course_info = json.loads(f.read())
    chapters = course_info.get('result').get('course_detail').get('terms')[term_index].get('chapter_info')[0] \
        .get('sub_info')
    return chapters

# 通过课程信息拼出播放页的url
def get_course_url(course):
    cid = course.get('cid')
    term_id = course.get('term_id')
    course_id = course.get('taid')
    url = 'https://ke.qq.com/webcourse/{}/{}#taid={}&vid={}'.format(cid, term_id, course_id, course.get('resid_list'))
    return url

#获取章节信息
def get_courses_from_chapter(chapter):
    return chapter.get('task_info')


