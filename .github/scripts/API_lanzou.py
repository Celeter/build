from lanzou.api import LanZouCloud
import os

lzy = LanZouCloud()


def get_result(code):
    if code == LanZouCloud.SUCCESS:
        return 'OK'
    else:
        return f'NG errorCode:{code}'


def login(ylogin, phpdisk_info):
    print('开始登入')
    cookie = {'ylogin': ylogin, 'phpdisk_info': phpdisk_info}
    code = lzy.login_by_cookie(cookie)
    print('登入结果:', get_result(code))
    return code


def show_progress(file_name, total_size, now_size):
    percent = now_size / total_size
    bar_len = 60  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576), end='')


def handler(fid, is_file):
    if is_file:
        code = lzy.set_desc(fid, 'http://alanskycn.gitee.io/vip/', is_file=True)
        print('描述信息设置结果:', get_result(code))


def upload(path, id):
    print('开始上传文件')
    code = lzy.upload_file(path, id, callback=show_progress, uploaded_handler=handler)
    print('文件上传结果:', get_result(code))
    return code


def get_apk_path(path):
    if os.path.isfile(path):
        return path
    else:
        file_list = os.listdir(path)
        for f in file_list:
            if os.path.splitext(f)[-1] == '.apk':
                return os.path.join(path, f)
        return os.path.abspath(path)


if __name__ == "__main__":
    if login(os.environ["LANZOU_ID"], os.environ["LANZOU_PSD"]) == LanZouCloud.SUCCESS:
        folder_name = os.environ["LANZOU_FOLDER"]
        print('文件夹名字:', folder_name)

        folders = lzy.get_move_folders()
        folder_id = folders.find_by_name(folder_name).id
        print('文件夹ID:', folder_id)

        flie_path = get_apk_path(os.environ["UPLOAD_FOLDER"])
        print('文件路径:', flie_path)

        try:
            if upload(flie_path, folder_id) == LanZouCloud.SUCCESS:
                info = lzy.get_share_info(folder_id, is_file=False)
                print(f'分享链接{info.url}')
                #print('\n分享链接:{}\n提取码:{}'.format(info.url, '无' if info.pwd == '' else info.pwd))
            else:
                print('第一次上传失败，再次上传')
                if upload(flie_path, folder_id) == LanZouCloud.SUCCESS:
                    info = lzy.get_share_info(folder_id, is_file=False)
                    print(f'分享链接{info.url}')
        except Exception as r:
            print(r)
                    #print('\n分享链接:{}\n提取码:{}'.format(info.url, '无' if info.pwd == '' else info.pwd))
