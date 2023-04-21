import cnocr
import re
from PIL import Image , ImageChops
from PIL.ImageShow import show
import openpyxl
import os
import warnings
import datetime
import numpy as np


def get_code(code_crop_img,ocr):
    # 获取图像大小
    width, height = code_crop_img.size
    # 查找背景颜色是(0, 0, 128)的像素
    bg_mask = Image.new(mode="1", size=(width, height))
    for x in range(width):
        for y in range(height):
            pixel = code_crop_img.getpixel((x, y))
            if pixel == (0, 0, 128):
                bg_mask.putpixel((x, y), 1)

    # 获取包含背景像素的最小矩形区域
    bbox = bg_mask.getbbox()
    x1 = bbox[0] - 100
    y1 = bbox[1] 
    x2 = bbox[2] 
    y2 = bbox[3] 
    target_box = (x1,y1,x2,y2)
    # 显示包含背景像素的最小矩形区域
    target_code= code_crop_img.crop(target_box)
    # target_code.show()
    # 将裁剪后的图片转换为灰度图像
    code_gray = target_code.convert('L')
    text = ocr.ocr(code_gray)
    code = -999
    if len(text) == 2: # [代码 , 名称 ]
        code = int(text[0]["text"])
    return code 


def convert(formatted_time):
  arrays = []
  warnings.filterwarnings('ignore')
  # 指定需要读取的文件夹路径
  folder_path = "截图"+formatted_time
  # 初始化cnocr模型
  ocr = cnocr.CnOcr()


  for filename in os.listdir(folder_path):
      if filename.endswith(".bmp"):
            # 读取原始图片
            img = Image.open(os.path.join(folder_path, filename))

            # 裁剪图片，仅保留需要识别的区域
            code_crop_img = img.crop((1180, 110, 1430, 965))
            code=get_code(code_crop_img,ocr)
            # print(code)

            deal_crop_img = img.crop((590, 140, 790, 340))
            # 将裁剪后的图片转换为灰度图像
            gray_img = deal_crop_img.convert('L')

            # 调用cnocr识别文字
            results = []
            results.append(code)
            text = ocr.ocr(gray_img)
            for i in text:
                my_str = i["text"]
                # print(my_str)
                if my_str.endswith("笔"):
                    numberslist = re.findall(r'\d+', my_str)
                    if len(numberslist) == 0:
                        numberslist = ['-999']
                    numbers = float(''.join(numberslist))
                    results.append(numbers)
            arrays.append(results)
  # 计算列表中数组的最大长度
  max_len = max([len(arr) for arr in arrays])

  # 将所有数组扩展到最大长度，并合并成一个多维矩阵
  data = np.array([np.pad(arr, (0, max_len - len(arr)), 'constant') for arr in arrays])

  data = data[data[:, 0].argsort()]

  # 保存 Excel 文件
  folder_path = "翻译"+formatted_time 
  file_name = "文本" + formatted_time + ".csv"
  file_path = os.path.join(folder_path, file_name)
  if not os.path.exists(folder_path):
      os.makedirs(folder_path)
  # 保存为csv文件
  np.savetxt(file_path, data, delimiter=',', fmt='%d')



def main():
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')  # 定义日期字符串的正则表达式
    formatted_time = input("请输入日期(格式为 yyyy-mm-dd,按下回车默认使用当前日期):").strip()
    if formatted_time == "":
        now = datetime.datetime.now() # 获取当前系统时间
        formatted_time = now.strftime("%Y-%m-%d") # 将时间格式化成字符串
        convert(formatted_time)
    elif not date_pattern.match(formatted_time):
        print("请输入正确格式日期")
    else:
        convert(formatted_time)

if __name__ == '__main__':
    main()