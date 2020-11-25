from lanzou.api import LanZouCloud
import os

# https://github.com/zaxtyson/LanZouCloud-API/blob/master/lanzou/api/core.py

lzy = LanZouCloud()


# print('正常:{}, URL错误:{}, 网络异常:{}, 文件已取消:{}, 缺少提取码:{}, 提取码错误:{}, 验证码错误:{}'.format(
# 	LanZouCloud.SUCCESS, LanZouCloud.URL_INVALID, LanZouCloud.NETWORK_ERROR, LanZouCloud.FILE_CANCELLED, 
# 	LanZouCloud.LACK_PASSWORD, LanZouCloud.PASSWORD_ERROR, LanZouCloud.CAPTCHA_ERROR))

def get_result(code):
    if code == LanZouCloud.SUCCESS:
        return '成功'
    else:
        return '失败'


def login():
    print('开始登入')
    ylogin = os.environ["LANZOU_ID"]
    phpdisk_info = os.environ["LANZOU_PSD"]
    cookie = {'ylogin': ylogin, 'phpdisk_info': phpdisk_info}
    code = lzy.login_by_cookie(cookie)
    print('login:', code)
    print('登入结果:', get_result(code))
    return code


def logout():
    print('开始登出')
    code = lzy.logout()
    print('logout:', code)
    print('登出结果:', get_result(code))
    return lcode


def set_max_size(size=500):
    print('开始设置单文件大小上限')
    # 设置单文件大小限制
    code = lzy.set_max_size(size)
    print('set_max_size:', code)
    print('设置单文件大小上限结果:', get_result(code))
    return code


def show_progress(file_name, total_size, now_size):
    print("进入进度回调函数")
    percent = now_size / total_size
    bar_len = 40  # 进度条长总度
    bar_str = '>' * round(bar_len * percent) + '=' * round(bar_len * (1 - percent))
    print('\r{:.2f}%\t[{}] {:.1f}/{:.1f}MB | {} '.format(
        percent * 100, bar_str, now_size / 1048576, total_size / 1048576, file_name), end='')
    if total_size == now_size:
        print('任务完成')


def handler(fid, is_file):
    print("进入上传回调函数")
    if is_file:
        # 设置描述信息
        code = lzy.set_desc(fid, 'Legado', is_file=True)
        print('描述信息设置结果:', get_result(code))
        # 设置提取码
        # code = lzy.set_passwd(fid, passwd='', is_file=True)
        # print('提取码设置结果:', get_result(code))


def upload(path, id):
    print('开始上传文件')
    code = lzy.upload_file(path, id, callback=show_progress, uploaded_handler=handler)
    print('upload:', code)
    print('文件上传结果:', get_result(code))
    return code


def get_dir_list():
    print('获取根路径文件夹列表')
    dirs = lzy.get_dir_list()
    print(dirs)


if __name__ == "__main__":
    if login() == LanZouCloud.SUCCESS:
        # set_max_size()

        # 要存放的文件夹名
        folder_name = os.environ["FOLDER_NAME"]
        print('文件夹名字:', folder_name)

        folders = lzy.get_move_folders()
        folder_id = folders.find_by_name(folder_name).id
        print('文件夹ID:', folder_id)

        flie_path = os.environ["FILE_PATH"]
        print('文件路径:', flie_path)

        # 解除大小限制
        lzy.ignore_limits()

        if upload(flie_path, folder_id) == LanZouCloud.SUCCESS:
            # 获取文件夹分享信息
            info = lzy.get_share_info(folder_id, is_file=False)
            print('\n分享链接:{}\n提取码:{}'.format(info.url, '无' if info.pwd == '' else info.pwd))
