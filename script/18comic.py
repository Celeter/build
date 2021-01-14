from PIL import Image
import requests
import hashlib, math, os


def downloadPic(url, path):
    with open(path, 'wb') as f:
        f.write(requests.get(url).content)


def processPic(path):
    img = Image.open(path)

    w = img.size[0]
    h = img.size[1]

    num = 10
    remainder = h % num
    copyW = w

    # 拼接前需要写拼接完成后的图片大小
    canvas = Image.new('RGB', img.size)

    for i in range(num):
        copyH = math.floor(h / num)
        py = copyH * i
        y = h - (copyH * (i + 1)) - remainder
        if i == 0:
            copyH = copyH + remainder
        else:
            py = py + remainder
        # 图片剪裁
        a = 0  # 图片距离左边的大小
        b = y  # 图片距离上边的大小
        c = a + copyW  # 图片距离左边的大小 + 图片自身宽度
        d = b + copyH  # 图片距离上边的大小 + 图片自身高度
        cropping = img.crop((a, b, c, d))
        # 图片拼接
        a = 0  # 图片距离左边的大小
        b = py  # 图片距离上边的大小
        c = a + copyW  # 图片距离左边的大小 + 图片自身宽度
        d = b + copyH  # 图片距离上边的大小 + 图片自身高度
        canvas.paste(cropping, (a, b, c, d))
    canvas.save(path)
    print(f'图片处理完成:{path}')


if __name__ == '__main__':
    url = 'https://cdn-msp.msp-comic.xyz/media/photos/230259/00020.jpg?v=1609559672'
    path = f'./{hashlib.md5(url.encode()).hexdigest()}.jpg'
    if os.path.isfile(path):
        pass
    else:
        downloadPic(url, path)
    processPic(path)
